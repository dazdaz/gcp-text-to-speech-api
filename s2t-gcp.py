#!/usr/bin/env python3

"""
Google Cloud Text-to-Speech Converter

This script converts text files to speech using Google Cloud Text-to-Speech API.

Prerequisites:
1. Install libraries: uv pip install google-cloud-texttospeech argparse
2. Install Google Cloud CLI: https://cloud.google.com/sdk/docs/install
3. Authenticate: gcloud auth application-default login
4. Set project: gcloud config set project YOUR_PROJECT_ID
5. Enable API: gcloud services enable texttospeech.googleapis.com

Usage:
  # Convert text to speech
  ./s2p-gcp.py input.txt output.mp3 --voice en-US-Wavenet-H --language en-US
  
  # List available voices
  ./s2p-gcp.py --list-voices --language en-US
"""

import argparse
import sys
from google.cloud import texttospeech


def list_voices(language_code):
    """
    List all available voices for a given language code.
    
    Args:
        language_code (str): Language code (e.g., 'en-US', 'es-ES')
    """
    try:
        client = texttospeech.TextToSpeechClient()
    except Exception as e:
        print(f"Error creating client: {e}")
        sys.exit(1)
    
    try:
        response = client.list_voices(language_code=language_code)
        
        print(f"\n{'='*60}")
        print(f"Available voices for language: {language_code}")
        print(f"{'='*60}\n")
        
        for voice in response.voices:
            print(f"Name: {voice.name}")
            print(f"Languages: {', '.join(voice.language_codes)}")
            print(f"Gender: {texttospeech.SsmlVoiceGender(voice.ssml_gender).name}")
            print(f"Natural Sample Rate: {voice.natural_sample_rate_hertz} Hz")
            print("-" * 60)
            
    except Exception as e:
        print(f"Error listing voices: {e}")
        sys.exit(1)


def text_to_speech(input_file, output_file, voice_name, language_code):
    """
    Convert text file to speech audio (MP3).
    
    Args:
        input_file (str): Path to input text file
        output_file (str): Path to output MP3 file
        voice_name (str): Voice name (e.g., 'en-US-Wavenet-D')
        language_code (str): Language code (e.g., 'en-US')
    """
    
    # Read the text from the input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        print(f"‚úì Read {len(text)} characters from '{input_file}'")
    except FileNotFoundError:
        print(f"‚úó Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"‚úó Error reading input file: {e}")
        sys.exit(1)

    # Create Text-to-Speech client
    try:
        client = texttospeech.TextToSpeechClient()
        print(f"‚úì Connected to Google Cloud Text-to-Speech API")
    except Exception as e:
        print(f"‚úó Error creating client: {e}")
        sys.exit(1)
    
    # Configure synthesis parameters
    synthesis_input = texttospeech.SynthesisInput(text=text)
    
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    print(f"‚úì Using voice: {voice_name} ({language_code})")

    # Perform the text-to-speech request
    try:
        print(f"‚ü≥ Synthesizing speech...")
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        print(f"‚úì Speech synthesis complete")
    except Exception as e:
        print(f"‚úó Error during synthesis: {e}")
        sys.exit(1)

    # Write the audio to output file
    try:
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
        print(f"‚úì Audio content written to '{output_file}'")
    except Exception as e:
        print(f"‚úó Error writing output file: {e}")
        sys.exit(1)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Text-to-Speech using Google Cloud API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert text to speech
  %(prog)s input.txt output.mp3 --voice en-US-Wavenet-H
  
  # List available voices
  %(prog)s --list-voices --language en-US
        """
    )
    
    parser.add_argument(
        'input_file',
        nargs='?',
        help="Input text file to convert to speech"
    )
    
    parser.add_argument(
        'output_file',
        nargs='?',
        help="Output MP3 file path"
    )
    
    parser.add_argument(
        '--list-voices',
        action='store_true',
        help="List available voices and exit"
    )
    
    parser.add_argument(
        '--voice',
        default="en-US-Wavenet-D",
        help="Voice name to use (default: en-US-Wavenet-D)"
    )
    
    parser.add_argument(
        '--language',
        default="en-US",
        help="Language code (default: en-US)"
    )

    args = parser.parse_args()

    # Execute appropriate function based on arguments
    if args.list_voices:
        list_voices(args.language)
    elif not args.input_file or not args.output_file:
        parser.print_help()
        sys.exit(1)
    else:
        text_to_speech(
            args.input_file,
            args.output_file,
            args.voice,
            args.language
        )


if __name__ == "__main__":
    main()

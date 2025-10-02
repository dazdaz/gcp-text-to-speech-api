# Code Explanation

This Python script converts text files to speech (MP3 audio) using **Google Cloud Text-to-Speech API**.

## What it does:

1. **Reads text** from an input file
2. **Sends the text** to Google Cloud's Text-to-Speech service
3. **Generates speech audio** using a selected voice
4. **Saves the audio** as an MP3 file
5. **Lists available voices** (optional feature)

## Google Cloud Text-to-Speech Converter

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

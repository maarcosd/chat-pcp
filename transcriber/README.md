# Transcriber

A Python service that converts audio files to text using Whisper and Google Cloud Storage.

## Features

- Fast and accurate audio transcription using Whisper JAX
- Google Cloud Storage integration for file handling
- Support for multiple audio formats
- Asynchronous processing for better performance
- Environment-based configuration

## Prerequisites

- Python 3.8+
- Google Cloud credentials
- Virtual environment (recommended)

## Installation

1. Clone the repository and navigate to the project directory:

```bash
git clone <repository-url>
cd transcriber
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your configuration values
   - Ensure your Google Cloud credentials are properly set up in `google_credentials.json`

## Configuration

The following environment variables need to be configured in your `.env` file:

- Google Cloud credentials and configuration
- API keys and service endpoints
- Other service-specific settings

## Usage

Run the transcriber service:

```bash
python app.py
```

## Project Structure

```
transcriber/
├── src/           # Source code
├── data/          # Data storage
├── app.py         # Main application entry point
├── requirements.txt
└── .env           # Environment configuration
```

## Dependencies

Key dependencies include:

- whisper-jax: For fast transcription
- google-cloud-storage: For cloud storage integration
- aiohttp: For async HTTP operations
- python-dotenv: For environment management

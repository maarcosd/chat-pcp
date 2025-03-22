# Parent AI Assistant

An AI-powered application to help parents better support their children's development through podcast content and interactive chat assistance.

## Features

- Interactive chat interface with AI assistance
- Episode list with detailed summaries
- Cheat sheets with key topics and tips
- Local file-based storage for podcast content
- Python microservice for additional functionality

## Prerequisites

- Node.js (v18 or higher)
- npm (v8 or higher)
- Python 3.8 or higher

## Setup

1. Install dependencies:

```bash
npm install
```

2. Set up the Python service:

```bash
cd python-service
python -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
pip install -r requirements.txt
```

3. Start the development servers:

```bash
npm run dev
```

This will start all the servers:

- Frontend: http://localhost:5173
- API: http://localhost:3000
- Python Service: http://localhost:8000

## Project Structure

```
.
├── frontend/               # React frontend application
│   ├── src/               # Source files
│   │   ├── App.tsx       # Main application component
│   │   └── ...
│   └── ...
├── api/                   # Node.js API application
│   ├── src/              # Source files
│   │   ├── server.ts     # Express server
│   │   └── ...
│   └── data/             # Local data storage
│       └── episodes.json # Episode data
├── python-service/        # Python microservice
│   ├── src/              # Source files
│   │   └── python_service/
│   │       └── main.py   # FastAPI application
│   └── requirements.txt  # Python dependencies
└── ...
```

## Development

- Frontend is built with React, TypeScript, and Tailwind CSS
- API uses Node.js with Express and TypeScript
- Python service uses FastAPI with Pydantic
- Chat interface uses assistant-ui library
- Local file storage for episode data

## Adding New Episodes

Add new episodes to `api/data/episodes.json` following the existing format:

```

```

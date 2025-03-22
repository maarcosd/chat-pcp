import os
from pathlib import Path

TRANSCRIPTS_BUCKET_NAME = "pcp-transcripts"
EPISODES_BUCKET_NAME = "pcp-episodes"
EMBEDDINGS_BUCKET_NAME = "pcp-embeddings"

# Latest episode tracking
LATEST_EPISODE_FILE = "latest_episode.txt"

# RSS Feed Configuration
RSS_FEED_URL = "https://feeds.simplecast.com/_7lcF_6g"

# Directory Configuration
PROJECT_ROOT = Path(__file__).parent.parent
EPISODES_DIR = f"{PROJECT_ROOT}/data/episodes"

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Google Cloud Configuration
GCP_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not GCP_CREDENTIALS:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set")

# ChromaDB Configuration
CHROMA_LOCAL_PATH = f"{PROJECT_ROOT}/data/chroma_db"
CHROMA_GCS_PATH = f"gs://{EMBEDDINGS_BUCKET_NAME}"

# Logging Configuration
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_LEVEL = "INFO"

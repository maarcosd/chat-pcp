import asyncio

from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Import after environment variables are loaded
from src.main import main

if __name__ == "__main__":
    asyncio.run(main())

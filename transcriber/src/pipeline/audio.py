import logging
from pathlib import Path
from typing import Optional

import aiohttp

logger = logging.getLogger(__name__)


class AudioDownloader:
    def __init__(self, episodes_dir: Path):
        self.episodes_dir = episodes_dir

    async def download(self, url: str, filename: str) -> Optional[Path]:
        """Download audio file from URL."""
        output_path = Path(self.episodes_dir) / "audio" / filename
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        logger.error(f"Failed to download audio: {response.status}")
                        return None

                    with open(output_path, "wb") as f:
                        f.write(await response.content.read())
                    logger.info(f"Downloaded MP3 file: {output_path}")
                    return output_path
        except Exception as e:
            logger.error(f"Error downloading audio: {e}")
            return None

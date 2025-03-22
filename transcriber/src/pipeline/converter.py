import logging
from datetime import timedelta
from typing import Dict

logger = logging.getLogger(__name__)


class TranscriptConverter:
    def _seconds_to_timestamp(self, seconds):
        return str(timedelta(seconds=int(seconds))).zfill(8)

    def convert(self, transcript: Dict) -> str:
        """Convert the transcript to a readable format."""
        try:
            chunks = transcript.get("chunks", [])

            output = ""

            for chunk in chunks:
                # Get timestamp and text
                start_time = chunk["timestamp"][0]
                text = chunk["text"].strip()

                # Convert timestamp to HH:MM:SS format
                timestamp = self._seconds_to_timestamp(start_time)

                # Write formatted line
                output += f"[{timestamp}] {text}\n"

            return output
        except Exception as e:
            logger.error(f"Error converting transcript: {e}")
            return None

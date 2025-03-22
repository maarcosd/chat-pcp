import json
import logging
import re
from pathlib import Path
from typing import Dict, Optional, TypedDict

from .audio import AudioDownloader
from .converter import TranscriptConverter
from .embedder import TranscriptEmbedder
from .filter import TransitionFilter
from .summary import SummaryGenerator
from .transcriber import Transcriber

logger = logging.getLogger(__name__)


class PipelineResult(TypedDict):
    raw_transcript: str
    converted_transcript: str
    summary: dict


class ProcessingPipeline:
    def __init__(self, episodes_dir: Path, openai_api_key: str):
        self.episodes_dir = episodes_dir
        self.downloader = AudioDownloader(episodes_dir)
        self.transcriber = Transcriber()
        self.converter = TranscriptConverter()
        self.filter = TransitionFilter()
        self.summarizer = SummaryGenerator(openai_api_key)
        self.embedder = TranscriptEmbedder()

    async def process_episode(self, episode: Dict) -> Optional[PipelineResult]:
        """Process an episode through the complete pipeline."""
        try:
            # Check for existing transcript
            transcript_path = (
                Path(self.episodes_dir) / f"transcripts/raw/{episode['slug']}.json"
            )
            if transcript_path.exists():
                audio_path = None
                logger.info(
                    f"Found existing transcript for episode: {episode['title']}"
                )
                with open(transcript_path) as f:
                    transcript = json.loads(f.read())
            else:
                # Step 1: Download
                logger.info(f"Downloading audio for episode: {episode['title']}")
                audio_path = await self.downloader.download(
                    episode["audio_url"],
                    f"{episode['slug']}.mp3",
                )
                if not audio_path:
                    logger.error(
                        f"Failed to download audio for episode: {episode['title']}"
                    )
                    return None

                # Step 2: Transcribe
                logger.info(f"Transcribing audio for episode: {episode['title']}")
                transcript = self.transcriber.transcribe(audio_path)
                if not transcript:
                    logger.error(
                        f"Failed to transcribe audio for episode: {episode['title']}"
                    )
                    return None

                # Save transcript for future use
                with open(transcript_path, "w") as f:
                    f.write(json.dumps(transcript, indent=4))

            # Step 3: Convert
            logger.info(f"Converting transcript for episode: {episode['title']}")
            converted_transcript = self.converter.convert(transcript)

            # Step 4: Filter repetitive transitions
            logger.info(f"Filtering transcript content for episode: {episode['title']}")
            filtered_transcript = self.filter.filter(converted_transcript)

            # Step 5: Summarize
            logger.info(f"Generating summary for episode: {episode['title']}")
            summary_data = self.summarizer.generate(filtered_transcript, episode)
            if summary_data:
                logger.info(
                    f"Successfully generated summary for episode: {episode['title']}"
                )
            else:
                logger.warning(f"No summary generated for episode: {episode['title']}")

            # Step 6: Embed
            logger.info(f"Embedding transcript for episode: {episode['title']}")
            self.embedder.process(episode, filtered_transcript)

            # Prepare result
            result: PipelineResult = {
                "raw_transcript": transcript,
                "converted_transcript": filtered_transcript,
                "summary": summary_data,
            }

            # Cleanup
            logger.info(f"Cleaning up temporary files for episode: {episode['title']}")
            if audio_path and audio_path.exists():
                audio_path.unlink()
            if transcript_path.exists():
                transcript_path.unlink()

            logger.info(
                f"Successfully completed processing for episode: {episode['title']}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Error in processing pipeline for {episode.get('title', 'unknown')}: {e}"
            )
            return None


__all__ = ["ProcessingPipeline"]

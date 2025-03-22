import asyncio
import json
import logging
import time
from typing import Dict

import aiohttp
from google.cloud import storage
from src.checkpoint import CheckpointManger
from src.pipeline import PipelineResult, ProcessingPipeline
from src.util import slugify_with_episode_number

from .config import (
    EPISODES_BUCKET_NAME,
    EPISODES_DIR,
    LOG_FORMAT,
    LOG_LEVEL,
    OPENAI_API_KEY,
    RSS_FEED_URL,
    TRANSCRIPTS_BUCKET_NAME,
)
from .feed_processor import FeedProcessor

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)


async def process_episode(
    processor: ProcessingPipeline, episode: Dict
) -> PipelineResult:
    """Process a single episode and log the results."""
    start_time = time.time()
    result = await processor.process_episode(episode)

    if result:
        duration = time.time() - start_time
        logger.info(f"Successfully processed episode: {episode['title']}")
        logger.info(f"Processing time: {duration / 60:.0f} minutes")
    else:
        logger.error(
            f"!!!!!!!!!!!! Failed to process episode: {episode['title']} !!!!!!!!!!!!"
        )

    return result


async def main():
    """Main function to run the episode processing pipeline."""
    try:
        # Initialize processors
        feed_processor = FeedProcessor(RSS_FEED_URL)
        episode_processor = ProcessingPipeline(EPISODES_DIR, OPENAI_API_KEY)

        storage_client = storage.Client()
        transcripts_bucket = storage_client.bucket(TRANSCRIPTS_BUCKET_NAME)
        episodes_bucket = storage_client.bucket(EPISODES_BUCKET_NAME)

        # Get the latest processed episode GUID
        checkpoint_manager = CheckpointManger(
            TRANSCRIPTS_BUCKET_NAME, "latest_episode.txt"
        )
        latest_guid = checkpoint_manager.get_checkpoint()
        logger.info(f"Latest processed episode GUID: {latest_guid}")

        # Process episodes from feed
        async for episode in feed_processor.find_episodes_to_process(latest_guid):
            episode["slug"] = slugify_with_episode_number(episode["title"])

            result = await process_episode(episode_processor, episode)

            if result:
                # Save raw transcript as JSON
                raw_transcript_blob = transcripts_bucket.blob(f"{episode['slug']}.json")
                raw_transcript_blob.upload_from_string(
                    json.dumps(result["raw_transcript"])
                )

                # Save converted transcript as text
                converted_transcript_blob = transcripts_bucket.blob(
                    f"{episode['slug']}-converted.txt"
                )
                converted_transcript_blob.upload_from_string(
                    result["converted_transcript"]
                )

                # Save episode with cheat sheet
                episode["cheat_sheet"] = result["summary"]
                episode_blob = episodes_bucket.blob(f"{episode['slug']}.json")
                episode_blob.upload_from_string(json.dumps(episode))

                # Update latest processed episode GUID
                checkpoint_manager.set_checkpoint(episode["guid"])
            else:
                logger.error(
                    "There was an error processing the episode, please fix and retry"
                )
                break

    except aiohttp.ClientError as e:
        logger.error(f"Network error while fetching feed: {e}")
        raise
    except ValueError as e:
        logger.error(f"Invalid data error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in main process: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())

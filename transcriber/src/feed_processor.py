import logging
import xml.etree.ElementTree as ET
from typing import AsyncGenerator, Optional

import aiohttp
from src.checkpoint import CheckpointManger

from .types import Episode

logger = logging.getLogger(__name__)


class FeedProcessor:
    """Processes the RSS feed and yields unprocessed episodes."""

    def __init__(self, feed_url: str):
        self._feed_url = feed_url
        self._namespaces = {"itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd"}

        ET.register_namespace("itunes", self._namespaces["itunes"])

    async def find_episodes_to_process(
        self, latest_guid: Optional[str] = None
    ) -> AsyncGenerator[Episode, None]:
        """Process RSS feed and yield unprocessed episodes."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self._feed_url) as response:
                    if response.status != 200:
                        raise aiohttp.ClientError(
                            f"Failed to fetch RSS feed: {response.status}"
                        )

                    feed_content = await response.text()
                    try:
                        root = ET.fromstring(feed_content)
                    except ET.ParseError as e:
                        raise ValueError(f"Invalid XML in feed: {e}")

                    channel = root.find("channel")
                    if channel is None:
                        raise ValueError(
                            "Invalid RSS feed format - no channel element found"
                        )

                    # Get all episodes from the feed
                    items = channel.findall("item")
                    if not items:
                        logger.info("No episodes found in feed")
                        return

                    found_latest = latest_guid is None
                    for item in reversed(items):
                        episode_guid = item.find("guid").text

                        if not found_latest:
                            if episode_guid == latest_guid:
                                found_latest = True
                                logger.info(
                                    "Found latest processed episode, starting from here"
                                )
                            continue

                        episode = self._parse_episode(item)
                        yield episode

                    logger.info("No new episodes found to process")

        except aiohttp.ClientError as e:
            logger.error(f"Network error processing RSS feed: {e}")
            raise
        except ValueError as e:
            logger.error(f"Feed format error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error processing RSS feed: {e}")
            raise

    def _parse_episode(self, item: ET.Element) -> Episode:
        """Parse an episode item from the RSS feed.

        Raises:
            ValueError: If required fields are missing from the episode.
        """
        # Required fields
        title_elem = item.find("title")
        if title_elem is None or not title_elem.text:
            raise ValueError("Episode missing required field: title")

        link_elem = item.find("link")
        if link_elem is None or not link_elem.text:
            raise ValueError("Episode missing required field: link")

        guid_elem = item.find("guid")
        if guid_elem is None or not guid_elem.text:
            raise ValueError("Episode missing required field: guid")

        enclosure = item.find("enclosure")
        if enclosure is None or not enclosure.get("url"):
            raise ValueError("Episode missing required field: audio_url")

        pub_date_elem = item.find("pubDate")
        if pub_date_elem is None or not pub_date_elem.text:
            raise ValueError("Episode missing required field: pub_date")

        # Optional fields with defaults
        summary_elem = item.find(f".//{{{self._namespaces['itunes']}}}summary")
        summary = summary_elem.text if summary_elem is not None else ""

        keywords_elem = item.find(f".//{{{self._namespaces['itunes']}}}keywords")
        keywords = (
            keywords_elem.text.split(",")
            if keywords_elem is not None and keywords_elem.text
            else []
        )

        duration_elem = item.find(f".//{{{self._namespaces['itunes']}}}duration")
        duration = (
            duration_elem.text
            if duration_elem is not None and duration_elem.text
            else "00:00:00"
        )

        return {
            "title": title_elem.text,
            "summary": summary,
            "pub_date": pub_date_elem.text,
            "link": link_elem.text,
            "audio_url": enclosure.get("url"),
            "guid": guid_elem.text,
            "keywords": keywords,
            "duration": duration,
        }

import re


def slugify_with_episode_number(title: str) -> str:
    """Convert title to URL-friendly slug with standardized episode number format.

    Takes a title like "Episode 42: Some Title" and converts it to "episode-042-some-title"
    """
    # First convert to lowercase and remove special chars
    slug = title.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)

    # Extract episode number if present
    episode_match = re.search(r"(?:episode|ep)\s*(\d+)", slug)
    if episode_match:
        episode_num = int(episode_match.group(1))
        # Remove the original episode reference
        slug = re.sub(r"(?:episode|ep)\s*\d+\s*", "", slug)
        # Add formatted episode number at start
        slug = f"episode-{episode_num:03d}-{slug}"

    # Clean up remaining whitespace/hyphens
    slug = re.sub(r"[-\s]+", "-", slug)
    return slug.strip("-")

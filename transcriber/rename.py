import os
import re


def normalize_episode_number(ep_num):
    # Convert episode number to 3-digit format
    return f"{int(ep_num):03d}"


def get_title_from_filename(filename):
    # Extract the title part from the filename
    # Remove the episode number prefix and -transcript-converted.txt suffix
    title = re.sub(r"^(ep|episode-|ep-)\d+[-_]", "", filename)
    title = re.sub(r"-transcript\.json\.json$", "", title)
    return title


def rename_transcript_files():
    episodes_dir = "data/episodes/transcripts/raw"

    # Get all transcript files
    transcript_files = [
        f for f in os.listdir(episodes_dir) if f.endswith("-transcript.json.json")
    ]

    for old_name in transcript_files:
        # Extract episode number
        ep_match = re.search(r"^(ep|episode-|ep-)(\d+)", old_name)
        if not ep_match:
            print(f"Could not extract episode number from {old_name}")
            continue

        ep_num = normalize_episode_number(ep_match.group(2))
        title = get_title_from_filename(old_name)

        # Create new filename
        new_name = f"episode-{ep_num}-{title}.json"

        # Rename file
        old_path = os.path.join(episodes_dir, old_name)
        new_path = os.path.join(episodes_dir, new_name)

        if old_path != new_path:
            print(f"Renaming: {old_name} -> {new_name}")
            os.rename(old_path, new_path)


if __name__ == "__main__":
    rename_transcript_files()

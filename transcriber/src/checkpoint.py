from asyncio.log import logger
from typing import Optional

from google.cloud import storage


class CheckpointManger:
    def __init__(self, bucket_name: str, file_name: str):
        self._file_name = file_name
        self._storage_client = storage.Client()
        self._bucket = self._storage_client.bucket(bucket_name)

    def get_checkpoint(self) -> Optional[str]:
        """Get the GUID of the latest processed episode from GCP."""
        try:
            blob = self._bucket.blob(self._file_name)
            if blob.exists():
                return blob.download_as_string().decode("utf-8").strip()
            return None
        except Exception as e:
            logger.error(f"Failed to read checkpoint file: {e}")
            return None

    def set_checkpoint(self, checkpoint: str) -> None:
        """Save the GUID of the latest processed episode to GCP."""
        try:
            checkpoint = checkpoint.strip()

            blob = self._bucket.blob(self._file_name)
            blob.upload_from_string(checkpoint)
            logger.info(f"Updated checkpoint with value: {checkpoint}")
        except Exception as e:
            logger.error(f"Failed to save checkpoint file: {e}")
            raise

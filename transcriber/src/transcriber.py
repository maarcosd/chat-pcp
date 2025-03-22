import logging
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel

logger = logging.getLogger(__name__)


class Transcriber:
    def __init__(
        self,
        model_name: str = "guillaumekln/faster-whisper-medium.en",
        language: str = "en",
        device: str = "cpu",
        compute_type: str = "float32",
    ):
        """Initialize the Whisper transcription model.

        Args:
            model_name: Name of the Whisper model to use
            language: Language code for transcription
            device: Device to run inference on ('cpu' or 'cuda')
            compute_type: Compute type for inference
        """
        self.model_name = model_name
        self.language = language
        # Initialize the model during construction
        try:
            self.model = WhisperModel(
                model_name,
                device=device,
                compute_type=compute_type,
            )
            logger.info(f"Successfully initialized Whisper model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Whisper model: {e}")
            raise

    def transcribe(self, audio_file_path: str) -> Dict:
        """Transcribe audio file, returning the transcription and segments.

        Args:
            audio_file_path: Path to the audio file to transcribe

        Returns:
            Dict containing:
                - text: Full transcription text
                - chunks: List of segments with text and timestamps

        Raises:
            FileNotFoundError: If audio file doesn't exist
            ValueError: If audio file is invalid or empty
            RuntimeError: If transcription fails
        """
        try:
            if not Path(audio_file_path).exists():
                raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

            audio, sampling_rate = self._preprocess_audio(audio_file_path)

            # Limit the audio to 10 seconds for testing
            audio = audio[: 10 * sampling_rate]

            if len(audio) == 0:
                raise ValueError(f"Audio file is empty: {audio_file_path}")

            # Transcribe the audio
            segments, _ = self.model.transcribe(
                audio,
                language=self.language,
                task="transcribe",
                vad_filter=True,
            )

            # Convert segments to a format similar to the original
            segments_list = []
            full_text = []

            for segment in segments:
                segments_list.append(
                    {"text": segment.text, "timestamp": (segment.start, segment.end)}
                )
                full_text.append(segment.text)

            return {
                "text": " ".join(full_text),
                "chunks": segments_list,
            }

        except (FileNotFoundError, ValueError) as e:
            logger.error(str(e))
            raise
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise RuntimeError(f"Failed to transcribe audio: {e}")

    def _preprocess_audio(self, audio_file_path: str) -> Tuple[np.ndarray, int]:
        """Preprocess audio file to the format required by Whisper.

        Args:
            audio_file_path: Path to the audio file

        Returns:
            Tuple of (audio_array, sampling_rate)

        Raises:
            ValueError: If audio preprocessing fails
        """
        try:
            audio, sampling_rate = sf.read(audio_file_path)

            # Convert to mono if stereo
            if len(audio.shape) > 1:
                audio = audio.mean(axis=1)

            # Resample to 16kHz if needed (required by Whisper)
            if sampling_rate != 16000:
                audio = np.interp(
                    np.linspace(0, len(audio), int(len(audio) * 16000 / sampling_rate)),
                    np.arange(len(audio)),
                    audio,
                )
                sampling_rate = 16000

            # Convert to float32
            audio = audio.astype(np.float32)

            return audio, sampling_rate
        except Exception as e:
            raise ValueError(f"Error preprocessing audio: {str(e)}")

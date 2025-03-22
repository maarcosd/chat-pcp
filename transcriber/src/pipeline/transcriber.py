import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel


class Transcriber:
    def __init__(
        self,
        model_name: str = "guillaumekln/faster-whisper-medium.en",
        language: str = "en",
    ):
        self.model_name = model_name
        self.language = language
        # Initialize the model during construction
        self.model = WhisperModel(
            model_name,
            device="cpu",  # Can be changed to "cuda" for GPU inference
            compute_type="float32",
        )

    def transcribe(self, audio_file_path: str) -> dict:
        """Transcribe audio file, returning the transcription and segments."""
        try:
            audio, sampling_rate = self._preprocess_audio(audio_file_path)

            # Limit 30 seconds for testing
            # audio = audio[: (30 * sampling_rate)]

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

        except Exception as e:
            print(f"Fatal error in transcription: {e}")
            raise

    def _preprocess_audio(self, audio_file_path: str) -> tuple[np.ndarray, int]:
        """Preprocess audio file to the format required by Whisper."""
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

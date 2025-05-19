import sounddevice as sd
from scipy.io.wavfile import write
import whisper
from typing import Optional

class AudioProcessor:
    def __init__(self, model_name: str = "tiny", sample_rate: int = 16000, duration: int = 5):
        self.model = whisper.load_model(model_name)
        self.sample_rate = sample_rate
        self.duration = duration
        self.audio_file = "temp.wav"

    def record_audio(self) -> str:
        """Record audio for the specified duration and save to a file."""
        recording = sd.rec(int(self.duration * self.sample_rate), samplerate=self.sample_rate, channels=1)
        sd.wait()
        write(self.audio_file, self.sample_rate, recording)
        return self.audio_file

    async def transcribe_audio(self, audio_file: Optional[str] = None) -> str:
        """Transcribe audio to text using Whisper."""
        file_to_transcribe = audio_file or self.audio_file
        result = self.model.transcribe(file_to_transcribe, fp16=False)
        return result["text"]
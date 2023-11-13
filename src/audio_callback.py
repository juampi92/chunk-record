import numpy as np
import time


class AudioCallbackHandler:
    silence_threshold = 0.01  # Adjust based on testing
    sampling_rate = 16000  # Sampling rate for speech recognition
    pause_length = 3  # Pause length to consider for chunking

    def __init__(self, queue, pause_length=3):
        self.queue = queue
        self.recording = True
        self.current_audio_chunk = np.zeros((0,), dtype=np.float32)
        self.last_sound_time = time.time()
        self.pause_length = pause_length

    def stop_recording(self):
        if self.current_audio_chunk.size > 0:
            self.queue.put(self.current_audio_chunk)
            self.current_audio_chunk = np.zeros((0,), dtype=np.float32)
        else:
            self.queue.put(None)

        self.recording = False

    def callback(self, indata, frames, time_info, status):
        if status:
            print(f"Error: {status}")

        # Convert the buffer to float32 for compatibility with transcription model
        audio_buffer = indata[:, 0].astype(np.float32)

        # Check if the current audio buffer has sound
        if np.any(audio_buffer > self.silence_threshold):
            self.last_sound_time = time.time()
            self.current_audio_chunk = np.concatenate(
                (self.current_audio_chunk, audio_buffer)
            )
        elif time.time() - self.last_sound_time > self.pause_length:
            # Silence detected, enqueue the current audio for processing
            if self.current_audio_chunk.size > 0:
                self.queue.put(self.current_audio_chunk.copy())
                self.current_audio_chunk = np.zeros((0,), dtype=np.float32)
        else:
            # Still silent, continue collecting the audio
            self.current_audio_chunk = np.concatenate(
                (self.current_audio_chunk, audio_buffer)
            )

        # Handle recording stop
        if not self.recording:
            if self.current_audio_chunk.size > 0:
                self.queue.put(self.current_audio_chunk)
                self.current_audio_chunk = np.zeros((0,), dtype=np.float32)
            else:
                self.queue.put(None)

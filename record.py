import sounddevice as sd
import whisper
import threading
import queue
import argparse
import logging
import warnings
from src.audio_callback import AudioCallbackHandler
from src.device_selector import DeviceSelector
from src.dates_helper import log_initial_timestamp, log_final_timestamp

# Global variables
audio_queue = queue.Queue()
recording_state = {"recording": True}

# Create the parser
parser = argparse.ArgumentParser(description="Process some arguments.")

# Suppress specific warning
warnings.filterwarnings(
    "ignore", message="FP16 is not supported on CPU; using FP32 instead"
)

# Define arguments
parser.add_argument("--silent", action="store_true", help="Run in silent mode")
parser.add_argument("--microphone", type=str, help="Specify microphone", default="pick")
parser.add_argument("--debug", action="store_true", help="Debug mode")
parser.add_argument(
    "--pause-seconds",
    type=int,
    default=3,
    help="Amount of seconds to wait for silence before chunking audio",
)
parser.add_argument(
    "--model",
    type=str,
    default="small",
    help="Whisper model. https://pypi.org/project/openai-whisper/",
)

# Parse arguments
args = parser.parse_args()

audio_callback_handler = AudioCallbackHandler(
    queue=audio_queue, pause_length=args.pause_seconds
)

device_selector = DeviceSelector()

# Configuration
model_name = args.model


def get_logging_level(args):
    if args.silent:
        return logging.WARNING

    if args.debug:
        return logging.DEBUG

    return logging.INFO


# Set logging level
logging.basicConfig(level=get_logging_level(args), format="%(message)s")


# Thread function for transcription
def transcribe_audio(whisper_model):
    start_time = log_initial_timestamp()

    while recording_state["recording"] or not audio_queue.empty():
        audio_chunk = audio_queue.get()

        if audio_chunk is None:
            continue

        # Transcribe the audio_chunk
        result = whisper_model.transcribe(audio_chunk)

        # Trim the result:
        print(result["text"].strip())

    log_final_timestamp(start_time)
    logging.info("The end!")


# Set up the Whisper model
whisper_model = whisper.load_model(model_name)

# Start transcription thread
transcription_thread = threading.Thread(target=transcribe_audio, args=(whisper_model,))
transcription_thread.start()


# Select the device using the arguments
def select_device(device_selector, microphone, silent):
    if microphone == "default":
        return device_selector.select_default()

    if microphone == "pick" and silent:
        return device_selector.select_default()

    if microphone == "pick":
        return device_selector.cli_select()

    return device_selector.select_by_name(microphone)


device_index = select_device(device_selector, args.microphone, args.silent)

# Set your device sample rate
sample_rate = 16000

# Start recording
with sd.InputStream(
    callback=audio_callback_handler.callback,
    samplerate=sample_rate,
    device=device_index,
    channels=1,
):
    logging.info("Audio capturing ready, start talking. Press enter to exit.")
    print("Start:")
    input()  # Wait for Enter key press to stop recording
    recording_state["recording"] = False
    audio_callback_handler.stop_recording()
    logging.info("Stopping recording")

# Wait for the transcription thread to finish
transcription_thread.join()

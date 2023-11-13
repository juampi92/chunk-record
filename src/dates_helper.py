from datetime import datetime
import logging


def get_time_formatted(dt=None):
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%H:%M:%S")


def log_initial_timestamp():
    start_time = datetime.now()
    logging.info(f"Audio started at: {get_time_formatted(start_time)} hs\n\n")
    return start_time


def log_final_timestamp(start_time):
    end_time = datetime.now()
    duration = end_time - start_time
    logging.info(f"\nAudio ended at: {get_time_formatted(end_time)} hs\n")
    logging.info(
        f"Duration: {duration.seconds//3600:02d}:{(duration.seconds//60)%60:02d}:{duration.seconds%60:02d}\n"
    )

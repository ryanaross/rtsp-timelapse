import datetime
import subprocess
from time import sleep
import json
import config
import logging
from suntime import Sun
from make_still import capture_image
from make_video import create_video
from make_timelapse import create_timelapse

logging.basicConfig(level=config.logging_level, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

def load_last_run_times():
    try:
        with open('data/last_run_times.json', 'r') as f:
            times = json.load(f)
            return datetime.datetime.fromisoformat(times['still']), datetime.datetime.fromisoformat(times['video']), datetime.datetime.fromisoformat(times['timelapse'])
    except FileNotFoundError:
        return datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now()

def save_last_run_times(still_time, video_time, timelapse_time):
    with open('data/last_run_times.json', 'w') as f:
        json.dump({'still': still_time.isoformat(), 'video': video_time.isoformat(), 'timelapse': timelapse_time.isoformat()}, f)

def main():
    last_still_time, last_video_time, last_timelapse_time = load_last_run_times()

    if config.launch_webserver:
        subprocess.Popen(["python", "webserver.py"])

    while True:
        current_time = datetime.datetime.now()
                
        # Make a video from the stills every x seconds, but only overnight if config.daytime is True, otherwise anytime is fine
        if (current_time - last_video_time).total_seconds() >= config.video_interval and (not config.daytime or (config.daytime and 0 <= current_time.hour < 6)):
            logging.info('Generating video...')
            create_video(delete_stills=True)
            last_video_time = current_time
            logging.info('Video generated.')

        # Every x seconds combine the videos into a single timelapse file, but only overnight if config.daytime is True, otherwise anytime is fine
        if (current_time - last_timelapse_time).total_seconds() >= config.timelapse_interval and (not config.daytime or (config.daytime and 0 <= current_time.hour < 6)):
            logging.info('Generating timelapse...')
            create_timelapse(delete_videos=True)
            last_timelapse_time = current_time
            logging.info('Timelapse generated.')

        # Generate stills every x seconds
        if (current_time - last_still_time).total_seconds() >= config.still_interval:
            if config.daytime:
                sun = Sun(config.latitude, config.longitude)

                sunrise = sun.get_local_sunrise_time(current_time)
                sunset = sun.get_local_sunset_time(current_time)

                if sunrise.time() <= current_time.time() <= sunset.time():
                    capture_image()
                    last_still_time = current_time
                    logging.info('Generated still')
            else:
                capture_image()
                last_still_time = current_time
                logging.info('Generated still')

        save_last_run_times(last_still_time, last_video_time, last_timelapse_time)

        # Sleep for a minute before checking again
        sleep(60)

if __name__ == "__main__":
    main()
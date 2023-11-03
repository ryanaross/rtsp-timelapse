import os
import logging

from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env in development
load_dotenv(find_dotenv())

# Required
rtsp_stream_url = os.environ.get('rtsp_stream_url', 'default_url')

 # Optional
camera_title = os.environ.get('camera_title', 'Default Camera')

add_timestamp_str = os.environ.get('add_timestamp', 'False')
add_timestamp = False if add_timestamp_str.lower() == 'false' else bool(add_timestamp_str)

daytime_str = os.environ.get('daytime', 'True') # only record stills during daytime
daytime = False if daytime_str.lower() == 'false' else bool(daytime_str)

still_interval = int(os.environ.get('still_interval', 300))  # default is 5 minutes
video_interval = int(os.environ.get('video_interval', 86400))  # default is 1 day
timelapse_interval = int(os.environ.get('timelapse_interval', 2592000))  # default is 30 days

# these values are used for sunrise/sunset times
latitude = float(os.environ.get('latitude', 37.7749))
longitude = float(os.environ.get('longitude', -122.4194))
timezone = os.environ.get('timezone', 'US/Pacific')

fps = int(os.environ.get('fps', 10)) # how many stills per second to make the videos
bitrate = os.environ.get('bitrate', "2000k") # bitrate for the compressed videos

logging_level_str = os.environ.get('logging_level', 'DEBUG')
logging_level = getattr(logging, logging_level_str)

launch_webserver_str = os.environ.get('launch_webserver', 'True')
launch_webserver = False if launch_webserver_str.lower() == 'false' else bool(launch_webserver_str)

webserver_port = int(os.environ.get('webserver_port', 5000))
import argparse

def create_timelapse(delete_videos=False):
    """
    make_timelapse.py

    This script creates a timelapse video from a series of videos. It assumes all videos are the same size.

    Usage:
        create_timelapse(delete_videos=False)

    Arguments:
        delete_videos: Optional. If this argument is True, the script will delete the original videos after creating the timelapse.

    """

    import os
    import glob
    import logging
    from moviepy.editor import concatenate_videoclips, VideoFileClip
    import config

    logging.basicConfig(level=config.logging_level, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

    videos_dir = './videos/'
    timelapse_dir = './timelapse/'

    # get all the video files in the videos directory
    video_files = sorted([f for f in glob.glob(
        videos_dir + "*.mp4") if os.path.isfile(f)])
    logging.debug(
        f"Found {len(video_files)} video files in {videos_dir}: {video_files}")

    # if there aren't any image_files, exit the program
    if not video_files:
        return

    # concatenate all the videos
    clips = [VideoFileClip(video) for video in video_files]
    final_clip = concatenate_videoclips(clips)
    logging.debug(f"All videos in {videos_dir} concatenated: {video_files}")

    # specify the output video file
    first_video_name = os.path.splitext(
        os.path.basename(video_files[0]))[0].split('-')[0]
    last_video_name = os.path.splitext(
        os.path.basename(video_files[-1]))[0].split('-')[1]
    video_name = first_video_name + '-' + last_video_name + '.mp4'
    video_path = timelapse_dir + video_name

    final_clip.write_videofile(video_path)
    logging.debug(f"Final video written to file at {video_path}.")

    # delete the original videos if delete_videos argument is True
    if delete_videos:
        for video_file in video_files:
            os.remove(video_file)
            logging.debug(f"Original video {video_file} in {videos_dir} deleted.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a timelapse video from a series of videos.')
    parser.add_argument('--delete_videos', action='store_true', help='Delete the original videos after creating the timelapse.')
    args = parser.parse_args()

    create_timelapse(delete_videos=args.delete_videos)
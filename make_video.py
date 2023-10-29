import argparse


def create_video(delete_stills=False):
    """
    make_video.py

    This script creates a video from a series of still images. It assumes all images are the same size.

    Usage:
        create_video(delete_stills=False)

    Arguments:
        delete_stills: Optional. If this argument is True, the script will delete the still images after creating the video.

    """

    import os
    import glob
    import logging
    import config

    from os.path import isfile
    from moviepy.editor import ImageSequenceClip, concatenate_videoclips

    logging.basicConfig(level=config.logging_level, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

    stills_dir = './stills/'
    videos_dir = './videos/'

    # get all the image files in the stills directory
    image_files = sorted([f for f in glob.glob(os.path.join(stills_dir, "*.jpg")) if isfile(f)])
    logging.debug(f"Found {len(image_files)} image files.")

    # if there aren't any image_files, exit the program
    if not image_files:
        return

    # specify the output video file
    first_image_name = os.path.splitext(os.path.basename(image_files[0]))[0]
    last_image_name = os.path.splitext(os.path.basename(image_files[-1]))[0]
    video_name = first_image_name + '-' + last_image_name + '.mp4'
    video_path = os.path.join(videos_dir, video_name)
    logging.debug(f"Output video file: {video_path}")

    # create a list of image clips
    clip = ImageSequenceClip(stills_dir, fps=config.fps)

    clip.write_videofile(video_path, codec='libx264', fps=config.fps, bitrate=config.bitrate, ffmpeg_params=["-g", str(config.fps)])

    # check if the video was successfully created
    if isfile(video_path):
        logging.info(f"Video successfully created at {video_path}.")
        # delete the stills that were used only if 'delete_stills' argument is True
        if delete_stills:
            for image_file in image_files:
                os.remove(image_file)
                logging.debug(f"Deleted {image_file}.")
    else:
        logging.error('Unable to create the video')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a video from a series of still images.')
    parser.add_argument('--delete_stills', action='store_true', help='Delete the still images after creating the video.')
    args = parser.parse_args()

    create_video(delete_stills=args.delete_stills)
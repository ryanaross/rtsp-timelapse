import argparse

def capture_image():
    import cv2
    from datetime import datetime
    import logging
    import config
    import shutil

    logging.basicConfig(level=config.logging_level, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

    # use the rtsp stream url from the config file
    rtsp_stream_url = config.rtsp_stream_url
    add_timestamp = config.add_timestamp
    stills_dir = './stills/'

    # create a VideoCapture object
    cap = cv2.VideoCapture(rtsp_stream_url)

    # check if the stream is opened
    if cap.isOpened():
        # read the frame from the stream
        ret, frame = cap.read()
        if ret:
            # specify the path to save the image
            # name the image after the current date and time
            image_name = datetime.now().strftime('%Y%m%d_%H%M%S') + '.jpg'
            image_path = stills_dir + image_name

            # put timestamp on the image if config option is set
            if add_timestamp:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, timestamp, (10, frame.shape[0] - 10), font, 1, (255, 255, 255), 2)

            # save the image
            cv2.imwrite(image_path, frame)
            logging.info(f"Image saved at {image_path}")

            # also save the image as latest.jpg
            shutil.copy2(image_path, stills_dir + 'latest.jpg')
        else:
            logging.error('Unable to read frame from stream')
    else:
        logging.error('Unable to open the stream')

    # release the VideoCapture object
    cap.release()
    logging.debug("VideoCapture object released.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Capture an image from the RTSP stream.')
    args = parser.parse_args()

    capture_image()
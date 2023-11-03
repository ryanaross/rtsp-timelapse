from flask import Flask, send_file, render_template, Response
import glob
import os
import logging
import config
from datetime import datetime
import mimetypes
import subprocess


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

app = Flask(__name__)

@app.route('/')
def serve_status():
    logging.debug('Serving status...')
    directories = ['stills', 'videos', 'timelapse']
    directories_info = []
    for directory in directories:
        logging.debug(f'Processing directory: {directory}')
        files = glob.glob(f'{directory}/*')
        file_count = len(files)
        latest_file = max(files, key=os.path.getctime) if files else None
        latest_modified_time = (
            datetime.fromtimestamp(os.path.getmtime(latest_file)).strftime('%Y-%m-%d %H:%M')
            if latest_file
            else None
        )
        directories_info.append({
            'directory': directory,
            'file_count': file_count,
            'latest_file': latest_file,
            'latest_modified_time': latest_modified_time
        })
    stills = glob.glob('stills/*')
    latest_image = max(stills, key=os.path.getctime) if stills else None
    config_variables = {name: value for name, value in config.__dict__.items() if not name.startswith('__')}
    return render_template('status.html', directories=directories_info, latest_image=latest_image, config_variables=config_variables)


@app.route('/make_video', methods=['POST'])
def make_video():
    logging.debug('Making video...')
    # Run the make_video.py script
    subprocess.run(["python", "make_video.py"], check=True)

    # Get the most recent file in the videos directory
    video_files = glob.glob('videos/*')
    if not video_files:
        return 'No video files found', 404

    latest_video_file = max(video_files, key=os.path.getctime)

    if os.path.exists(latest_video_file):
        with open(latest_video_file, 'rb') as f:
            data = f.read()
        response = Response(data, mimetype='video/mp4')
        response.headers['Content-Disposition'] = 'attachment; filename={}'.format(os.path.basename(latest_video_file))
        os.remove(latest_video_file)  # Delete the file after sending it
        logging.debug(f'Removing video at {latest_video_file}')
        return response
    else:
        return 'Video not found', 404

@app.route('/files/<path:directory>')
def serve_file_list(directory):
    logging.debug(f'Serving file list for directory: {directory}')
    # Check if the directory exists
    if os.path.exists(directory):
        # Get a list of files in the directory
        files = glob.glob(f'{directory}/*')
        
        # Sort the files by their modified times in descending order
        files_sorted = sorted(files, key=os.path.getmtime, reverse=True)

        # Create a dictionary with file names as keys, their last modified dates and sizes (rounded to nearest integer in KB) as values
        files_dict = {file: {'last_modified': datetime.fromtimestamp(os.path.getmtime(file)).strftime('%Y-%m-%d %H:%M'), 'size': round(os.path.getsize(file) / 1024)} for file in files_sorted}
        
        # Render the template with the dictionary of files, their last modified dates and sizes
        return render_template('file_list.html', files=files_dict)
    else:
        # Return a 404 error if the directory does not exist
        return 'Directory not found', 404

@app.route('/media/<path:filename>', methods=['DELETE'])
def delete_media(filename):
    # Check if the file exists
    if os.path.exists(filename):
        # Delete the file
        os.remove(filename)
        return 'File deleted', 200
    else:
        # Return a 404 error if the file does not exist
        return 'File not found', 404

@app.route('/media/<path:filename>')
def serve_media(filename):
    # Check if the file exists
    if os.path.exists(filename):
        # Auto-detect mimetype
        mimetype, encoding = mimetypes.guess_type(filename)
        
        # Serve the file using send_file
        return send_file(filename, mimetype=mimetype)
    else:
        # Return a 404 error if the file does not exist
        return 'File not found', 404

def start_flask_app():
    logging.debug('Starting Flask app...')
    app.run(host='0.0.0.0', port=5000)
    logging.debug('Exiting flask app.')

if __name__ == "__main__":
    logging.debug('Running webserver.py...')
    start_flask_app()
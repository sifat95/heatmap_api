import os
import urllib.request
from app import app
from flask import Flask, request, redirect, jsonify, send_from_directory, abort
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file-serve/<path:filename>')
def upload_file(filename):
	# check if filename is empty
	if filename == '':
		resp = jsonify({'message' : 'File '})
		resp.status_code = 400
		return resp
	if allowed_file(filename):
		try:
			send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=False)
			resp = jsonify({'message' : 'File successfully served'})
			resp.status_code = 201
			return resp
		except FileNotFoundError:
			abort(404)
	else:
		resp = jsonify({'message' : 'Allowed file type is png'})
		resp.status_code = 400
		return resp

if __name__ == "__main__":
    app.debug = True
    app.run()
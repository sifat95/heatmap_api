import os
import urllib.request

from flask import Flask, request, redirect, jsonify, send_from_directory, abort

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

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
			return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
		except FileNotFoundError:
			abort(404)
	else:
		resp = jsonify({'message' : 'Allowed file type is png'})
		resp.status_code = 400
		return resp

if __name__ == "__main__":
    app.debug = True
    app.run()

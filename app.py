from flask import Flask, request, jsonify, send_from_directory, abort, render_template
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_IP = '20.218.226.24'


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.before_request
def limit_remote_addr():
    client_ip = request.remote_addr
    if client_ip != ALLOWED_IP:
        abort(403, description="Forbidden: Your IP is not allowed")

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return jsonify({'message': 'Image uploaded', 'filename': file.filename})

@app.route('/images', methods=['GET'])
def list_images():
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify(files)

@app.route('/uploads/<filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/images/<filename>', methods=['DELETE'])
def delete_image(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({'message': f'{filename} deleted'})
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

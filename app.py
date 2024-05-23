from flask import Flask, request, render_template, jsonify
from color_init import *
import logging
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'static/gallery'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/color", methods=['POST'])
def colorize():
    try:
        display_images(images)
        return jsonify(success=True, message="Photos colorized")
    except Exception as ex:
        return jsonify(success=False, message=str(ex))
    
@app.route("/gallery")
def gallery():
    try:
        image_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(('.jpg'))]
        if not image_files:
            return render_template("no_files.html")
        files = []
        for image_file in image_files:
            files.append({'filename' : image_file})
        return render_template("gallery.html", image_files=files)
    except Exception as ex:
        logging.error(f"Error in finding images: {ex}")
        return render_template("error.html")
    
@app.route("/delete_image/<filename>", methods=['DELETE'])
def delete_image(filename):
    try:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        os.remove(filepath)
        return jsonify(success=True, message="Image deleted successfully")
    except Exception as ex:
        return jsonify(success=False, message=str(ex))

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0")

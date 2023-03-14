import os
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

from pdfparse.pdf_parsing import mine_pdf

app = Flask("pdfparse")

app.config.update({"DEFAULT_FOLDER": Path(__file__).parent / "data"})


def list_saved_files():
    return os.listdir(app.config.get("DEFAULT_FOLDER"))


def save_file(file_bytes, filename):
    full_name = app.config.get("DEFAULT_FOLDER") / filename
    file_bytes.save(full_name)
    return full_name


@app.route("/saved", methods=["GET"])
def get_saved_file_names():
    return jsonify({"known_files": list_saved_files()}), 200


@app.route("/saved/<filename>", methods=["GET"])
def parse_saved_pdf(filename):
    if filename not in list_saved_files():
        return f"File {filename} not found. Are you sure you uploaded it?", 404
    else:
        return jsonify(mine_pdf(app.config.get("DEFAULT_FOLDER") / filename)), 200


@app.route("/saved/<filename>", methods=["DELETE"])
def delete_saved_file(filename):
    if filename not in list_saved_files():
        return f"File {filename} not found. Are you sure you uploaded it?", 404
    else:
        os.remove(app.config.get("DEFAULT_FOLDER") / filename)
        return f"File {filename} successfully removed", 200


@app.route("/", methods=["POST", "PUT"])
def upload_and_parse_pdf():
    """
    Parse an uploaded pdf file. If the method is POST, the file also gets saved
    :return: List of strings corresponding to read chunks.
    """

    if "file" not in request.files:
        return "Request must contain a file", 400
    file = request.files["file"]
    if file.mimetype != "application/pdf":
        return "Only .pdf files are allowed", 400

    if request.method == "PUT":
        filename = f"temp_file_{datetime.now()}.pdf"
    else:
        filename = file.filename.split("/")[-1]

    saved_name = save_file(file, secure_filename(filename))
    text_chunks = mine_pdf(saved_name)
    if request.method == "PUT":
        os.remove(saved_name)
    return jsonify(text_chunks), 200

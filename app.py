from flask import Flask, request, render_template, jsonify
from azure.storage.blob import BlobServiceClient
import os

app = Flask(__name__)

# Azure Storage configuration (replace with your credentials)
AZURE_STORAGE_CONNECTION_STRING = "your_connection_string"
CONTAINER_NAME = "your_container_name"

# Blob service client
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)


@app.route("/")
def index():
    """
    Serve the HTML front end.
    """
    return render_template("index.html")


@app.route("/upload-files", methods=["POST"])
def upload_files():
    """
    Upload three files (two txt and one xml) to ADLS.
    """
    if "file1" not in request.files or "file2" not in request.files or "file3" not in request.files:
        return jsonify({"status": "error", "message": "Please upload all three files"}), 400

    file1 = request.files["file1"]
    file2 = request.files["file2"]
    file3 = request.files["file3"]

    # Validate file types
    if not (file1.filename.endswith(".txt") and file2.filename.endswith(".txt") and file3.filename.endswith(".xml")):
        return jsonify({"status": "error", "message": "File types must be 2 .txt and 1 .xml"}), 400

    # Upload files to ADLS
    try:
        files = [file1, file2, file3]
        for file in files:
            blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file.filename)
            # Upload the file
            blob_client.upload_blob(file.read(), overwrite=True)
        return jsonify({"status": "success", "message": "Files uploaded successfully"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error uploading files: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)

import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import threading
import generate_process

# Use relative paths for portability
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'User_Uploads')
STATIC_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
REELS_FOLDER = os.path.join(STATIC_FOLDER, 'reels')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'mov', 'avi'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size

# Ensure the upload and reels folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(REELS_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_reel_async(rec_id):
    """Process reel generation in background thread"""
    try:
        print(f"Starting background processing for {rec_id}")
        generate_process.text_to_audio(rec_id)
        generate_process.create_reel(rec_id)
        print(f"Completed processing for {rec_id}")
    except Exception as e:
        print(f"Error processing reel {rec_id}: {str(e)}")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    my_id = str(uuid.uuid1())
    if request.method == "POST":
        rec_id = request.form.get("uuid", my_id)
        description = request.form.get("text", "")
        
        if not description.strip():
            return render_template("create.html", my_id=my_id, error="Please provide a description")
        
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], rec_id)
        os.makedirs(folder_path, exist_ok=True)

        input_files = []
        # Process all uploaded files
        for key in request.files:
            file = request.files[key]
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(folder_path, filename)
                file.save(file_path)
                input_files.append(filename)
                print(f"Saved file: {filename}")

        if not input_files:
            return render_template("create.html", my_id=my_id, error="Please upload at least one valid file")

        # Save description
        with open(os.path.join(folder_path, "description.txt"), "w", encoding="utf-8") as f:
            f.write(description)

        # Save input.txt for ffmpeg concat
        with open(os.path.join(folder_path, "input.txt"), "w", encoding="utf-8") as f:
            for fl in input_files:
                f.write(f"file '{fl}'\nduration 1\n")
            # Repeat last file to avoid 0:00 video
            if input_files:
                f.write(f"file '{input_files[-1]}'\n")
        
        # Start the generation process in background thread
        thread = threading.Thread(target=process_reel_async, args=(rec_id,))
        thread.daemon = True
        thread.start()
        
        # Redirect to gallery with success message
        return redirect(url_for('gallery', success='true'))

    return render_template("create.html", my_id=my_id)

@app.route("/gallery")
def gallery():
    try:
        reels = [f for f in os.listdir(REELS_FOLDER) if f.endswith('.mp4')]
        # Sort by creation time, newest first
        reels.sort(key=lambda x: os.path.getctime(os.path.join(REELS_FOLDER, x)), reverse=True)
    except Exception as e:
        print(f"Error loading gallery: {e}")
        reels = []
    
    success = request.args.get('success', False)
    return render_template("gallery.html", reels=reels, success=success)

@app.route("/check_reel/<reel_id>")
def check_reel(reel_id):
    """API endpoint to check if a reel has been generated"""
    reel_path = os.path.join(REELS_FOLDER, f"{reel_id}.mp4")
    exists = os.path.exists(reel_path)
    return jsonify({"exists": exists})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
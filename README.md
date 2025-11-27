# AI Reel Generator - Fully Working Version

A Flask web application that automatically generates Instagram reels with AI-powered voiceovers using images/videos you upload.

## Features

✅ **Automatic Processing**: Upload files and description → audio generation → video creation happens automatically
✅ **Background Processing**: Non-blocking - you can navigate while reels are being created
✅ **Gallery Auto-Refresh**: Gallery page automatically updates when new reels are ready
✅ **Multiple File Upload**: Upload multiple images/videos for your reel
✅ **AI Voiceover**: Uses ElevenLabs API to generate professional voiceovers
✅ **Instagram Format**: Outputs videos in 1080x1920 (9:16 ratio) perfect for Instagram Reels

## Prerequisites

1. **Python 3.8+**
2. **FFmpeg** installed and added to system PATH
   - Windows: Download from https://ffmpeg.org/download.html
   - Mac: `brew install ffmpeg`a
   - Linux: `sudo apt install ffmpeg`
3. **ElevenLabs API Key** (sign up at https://elevenlabs.io)

## Installation

1. **Clone/Download the project**

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

3. **Update your ElevenLabs API Key**:
   - Open `test_to_audio.py`
   - Replace the `ELEVENLABS_API_KEY` with your actual API key

4. **Create required folders**:
The app will create these automatically, but you can create them manually:
```
static/
  reels/
  css/
User_Uploads/
templates/
```

## Project Structure

```
project/
│
├── main.py                  # Main Flask application (UPDATED)
├── generate_process.py      # Processing logic (UPDATED)
├── test_to_audio.py         # ElevenLabs integration
├── requirements.txt         # Python dependencies
│
├── templates/
│   ├── base.html           # Base template
│   ├── index.html          # Home page
│   ├── create.html         # Upload page (UPDATED)
│   └── gallery.html        # Gallery page (UPDATED)
│
├── static/
│   ├── css/
│   │   ├── style.css       # Main styles (UPDATED)
│   │   └── create.css      # Upload page styles (UPDATED)
│   └── reels/              # Generated reels (auto-created)
│
└── User_Uploads/            # Uploaded files (auto-created)
```

## Running the Application

1. **Start the Flask server**:
```bash
python main.py
```

2. **Open your browser**:
```
http://localhost:5000
```

## How to Use

1. **Navigate to "Create Reel"**
2. **Upload Files**: Click to select images/videos (you can add multiple files)
3. **Add Description**: Enter the text that will be converted to voiceover
4. **Click "Create Reel"**: 
   - You'll see a processing overlay
   - The page redirects to gallery automatically
   - Gallery auto-refreshes every 5 seconds for 2 minutes to show your new reel
5. **View in Gallery**: Your generated reel will appear in the gallery once ready

## How It Works

1. **Upload Phase**: User uploads files and enters description text
2. **Background Processing**:
   - Files are saved to `User_Uploads/{unique_id}/`
   - Description is saved as `description.txt`
   - File list is saved as `input.txt` (for FFmpeg)
3. **Audio Generation**: ElevenLabs API converts text to speech → `audio.mp3`
4. **Video Creation**: FFmpeg combines images/videos with audio → Instagram-format reel
5. **Output**: Final video saved to `static/reels/{unique_id}.mp4`

## Key Updates Made

### 1. **main.py**
- ✅ Added threading for background processing
- ✅ Fixed file upload handling
- ✅ Added proper error handling
- ✅ Added success/error messages
- ✅ Redirect to gallery after upload

### 2. **generate_process.py**
- ✅ Fixed all hardcoded paths (now uses relative paths)
- ✅ Added proper error handling and logging
- ✅ Fixed FFmpeg command formatting
- ✅ Proper path normalization for cross-platform compatibility

### 3. **create.html**
- ✅ Added form validation
- ✅ Added processing overlay during upload
- ✅ Better file input management
- ✅ Required fields validation
- ✅ Accept both images and videos

### 4. **gallery.html**
- ✅ Auto-refresh functionality (checks every 5 seconds)
- ✅ Success message after upload
- ✅ Download buttons for each reel
- ✅ Empty state when no reels exist
- ✅ Better video display with metadata

### 5. **CSS Files**
- ✅ Modern, responsive design
- ✅ Smooth animations and transitions
- ✅ Professional color scheme
- ✅ Mobile-friendly layout

## Troubleshooting

### FFmpeg not found
- Make sure FFmpeg is installed and in your system PATH
- Test by running `ffmpeg -version` in terminal

### Audio not generating
- Check your ElevenLabs API key is valid
- Check API quota/limits

### Reel not appearing in gallery
- Wait 30-60 seconds for processing
- Check console logs for errors
- Verify FFmpeg is working correctly

### Files not uploading
- Check file extensions are allowed (png, jpg, jpeg, mp4, mov, avi)
- Check file size (max 500MB per file)

## API Key Security Note

⚠️ **Important**: Never commit your actual API key to version control. Consider using environment variables:

```python
import os
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY', 'your-key-here')
```

## License

This is a demo project. Use at your own risk.

## Support

If you encounter issues:
1. Check the console logs
2. Verify all prerequisites are installed
3. Ensure folder permissions are correct
4. Check FFmpeg is working: `ffmpeg -version`

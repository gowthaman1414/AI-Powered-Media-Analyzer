# AI-Powered-Media-Analyzer

This is a Flask-based web application that allows users to summarize text, extract text from images, transcribe audio to text, and extract text from videos using AI-powered tools.

## Features

- **Text Summarization**: Summarize long text into a specified number of sentences.
- **Image Text Extraction**: Upload an image and extract text using Optical Character Recognition (OCR).
- **Audio Transcription**: Convert uploaded audio files into text using speech recognition.
- **Video Text Extraction**: Extract audio from a video and transcribe it into text.

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Bootstrap
- **OCR**: Tesseract OCR (via `pytesseract`)
- **Audio Transcription**: Google Speech Recognition API (via `SpeechRecognition`)
- **Video Processing**: `moviepy`
- **Text Summarization**: `sumy` (LSA algorithm)
- **File Handling**: Python's `os` and `werkzeug`

## Installation

### Prerequisites

- Python 3.x
- Pip (Python package installer)
- Tesseract OCR installed on your machine. [Installation instructions](https://github.com/tesseract-ocr/tesseract)

### Setup

1. Clone the repository

2. Create and activate a virtual environment
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up Tesseract (ensure it's installed and available in your system path).

5. Run the Flask application:
    ```bash
    python app.py
    ```

6. Open your browser and navigate to `http://127.0.0.1:5000`.

## Usage

### Homepage

The homepage provides four main functionalities:
1. **Summarize Text**: Input text and specify the number of sentences to generate a summary.
2. **Upload Image**: Upload an image, and the app will extract the text from the image.
3. **Upload Audio**: Upload an audio file, and the app will transcribe the audio to text.
4. **Upload Video**: Upload a video, and the app will extract audio from the video and transcribe it to text.

### Navigating

- Select one of the four features by clicking on the appropriate button.
- You will be taken to a new page where you can either input text or upload a file.

## Project Structure

```
/uploads               # Folder where uploaded files are stored
/static                # Static files (CSS, JavaScript, images)
    /css               # CSS files for styling
    /images            # Background or other images
/templates             # HTML templates for web pages
app.py                 # Main Flask application
requirements.txt       # Python dependencies
README.md              # This README file
```

## Requirements

The required packages can be found in the `requirements.txt` file. Some of the key dependencies include:
- Flask
- Tesseract OCR (`pytesseract`)
- MoviePy
- SpeechRecognition
- Sumy (Text Summarization)
- NLTK

## Future Improvements

- Add more advanced summarization algorithms.
- Support for additional audio and video formats.
- Improve user interface and mobile responsiveness.


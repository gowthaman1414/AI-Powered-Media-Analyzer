import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
import speech_recognition as sr
import moviepy.editor as mp
import requests

# Download the punkt tokenizer models
nltk.download('punkt')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Function to extract text from image using Tesseract OCR
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

recognizer = sr.Recognizer()

# Function to extract text from audio using SpeechRecognition
def extract_text_from_audio(filepath):
    with sr.AudioFile(filepath) as source:
        audio_data = recognizer.record(source)
    try:
        headers = {
            'authorization': "4439bc63c77b429d920d2bedcb4d2108",
            'content-type': 'application/json'
        }
        upload_url = "https://api.assemblyai.com/v2/upload"
        def read_file(file_path):
            with open(file_path, 'rb') as f:
                while True:
                    data = f.read(5242880)
                    if not data:
                        break
                    yield data
        response = requests.post(upload_url, headers=headers, data=read_file(filepath))
        if response.status_code == 200:
            audio_url = response.json()['upload_url']
            transcribe_url = "https://api.assemblyai.com/v2/transcript"
            json = {
                "audio_url": audio_url
            }
            response = requests.post(transcribe_url, json=json, headers=headers)
            if response.status_code == 200:
                transcript_id = response.json()['id']
                polling_url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
                while True:
                    response = requests.get(polling_url, headers=headers)
                    if response.json()['status'] == 'completed':
                        return response.json()['text']
                    elif response.json()['status'] == 'failed':
                        return "Transcription failed"
                    else:
                        import time
                        time.sleep(3)
        else:
            return f"Error uploading audio file: {response.text}"
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to extract text from video using moviepy
def extract_text_from_video(video_path):
    clip = mp.VideoFileClip(video_path)
    audio = clip.audio
    temp_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_audio.wav')
    audio.write_audiofile(temp_audio_path)
    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_audio_path) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    os.remove(temp_audio_path)
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['GET', 'POST'])
def summarize_page():
    if request.method == 'POST':
        text = request.form['text']
        num_sentences = int(request.form['num_sentences'])
        summary = get_summary(text, num_sentences)
        return render_template('summarize.html', summary=summary, original_text=text)
    return render_template('summarize.html')

@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image_page():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            text = extract_text_from_image(filepath)
            return render_template('upload_image.html', image_text=text)
    return render_template('upload_image.html')

@app.route('/upload_audio', methods=['GET', 'POST'])
def upload_audio_page():
    if request.method == 'POST':
        if 'audio' not in request.files:
            return "No audio file found", 400
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return "No selected file", 400
        file_path = os.path.join(app.root_path, 'uploads', audio_file.filename)
        audio_file.save(file_path)
        extracted_text = extract_text_from_audio(file_path)
        if extracted_text:
            return render_template('upload_audio.html', audio_text=extracted_text)
        else:
            return "Text extraction failed", 500
    return render_template('upload_audio.html')

@app.route('/upload_video', methods=['GET', 'POST'])
def upload_video_page():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            text = extract_text_from_video(filepath)
            return render_template('upload_video.html', video_text=text)
    return render_template('upload_video.html')

def get_summary(text, sentences_count):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count)
    summary_text = " ".join(str(sentence) for sentence in summary)
    return summary_text

if __name__ == '__main__':
    app.run(debug=True)

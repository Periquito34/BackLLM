import fitz  # PyMuPDF
import io
import docx
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import google.generativeai as genai
from genDOCX import generate_docx
import os
import glob
from docx import Document
from lecturaArchivos import read_pdf, read_docx, classify_requirements

app = Flask(__name__)
CORS(app)

genai.configure(api_key="API-KEY")
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def index():
    return "API is running"

@app.route('/generate-questions', methods=['POST'])
def generate_questions():
    context = request.json.get('context')
    try:
        generated_text = generate_text(f"¿Qué tipo de preguntas puedo hacerle a mi cliente para comprender mejor sus necesidades?, en este caso es una entrevista con un cliente para la extracción de requerimientos, (Tienen que ser preguntas no tan técnicas, amigables para el cliente) Context: {context}")
        questions = generated_text.split('\n')  
        return jsonify({'questions': questions})
    except Exception as e:
        error_message = f"Error during request: {e}"
        return jsonify({'error': error_message}), 500

def classify_requirements2(text, genai):
    prompt = f"Generate user stories from the following requirements:\n\n{text}"
    response = genai.GenerativeModel('gemini-pro').generate_content(prompt)
    if response and response._result and response._result.candidates:
        generated_content = response._result.candidates[0].content.parts[0].text
        return generated_content
    return ""

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "Unsupported file type"}), 400

    text = read_pdf(file)
    user_stories = classify_requirements2(text, genai)

    output_path = "generated_files/processed_requirements.docx"
    with open(output_path, 'w') as doc:
        doc.write(user_stories)
    
    return jsonify({"message": "PDF processed successfully", "output_path": output_path})

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file.filename.endswith('.pdf'):
        text = read_pdf(file)
    elif file.filename.endswith('.docx'):
        text = read_docx(file)
    else:
        return jsonify({"error": "Unsupported file type"}), 400

    requirements = classify_requirements(text, genai)

    output_path = "generated_files/processed_requirements.docx"
    generate_docx(requirements, output_path)

    return jsonify({"message": "File processed successfully", "output_path": output_path})


def generate_text(prompt):
    response = model.generate_content(prompt)
    generated_text = response._result.candidates[0].content.parts[0].text
    return generated_text

if __name__ == '__main__':
    app.run(debug=True)

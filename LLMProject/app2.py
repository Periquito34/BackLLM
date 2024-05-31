from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from lecturaArchivos import read_pdf, read_docx, classify_requirements
from genPDF import generate_pdf


app = Flask(__name__)
CORS(app)  # Habilita CORS en toda la aplicación

genai.configure(api_key="API_KEY")
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def index():
    return "API is running"

@app.route('/generate-questions', methods=['POST'])
def generate_questions():
    context = request.json.get('context')
    try:
        generated_text = generate_text(f"¿Qué tipo de preguntas puedo hacerle a mi cliente para comprender mejor sus necesidades?, en este caso es una entrevista con un cliente para la estraccion de requerimientos, (Tienen que ser preguntas no tan tecnicas, amigables para el cliente) Context: {context}")
        questions = generated_text.split('\n')  
        return jsonify({'questions': questions})
    except Exception as e:
        error_message = f"Error durante la solicitud: {e}"
        return jsonify({'error': error_message}), 500
    

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

    output_path = "processed_requirements.pdf"
    generate_pdf(requirements, output_path)

    return jsonify({"message": "File processed successfully", "output_path": output_path})

def generate_text(prompt):
    response = model.generate_content(prompt)
    generated_text = response._result.candidates[0].content.parts[0].text
    return generated_text

if __name__ == '__main__':
    app.run(debug=True)

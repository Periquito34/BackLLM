from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # Habilita CORS en toda la aplicación

genai.configure(api_key="AIzaSyDrgS_nkCcezHkVGD2PeOAet-Ut9fPOuAc")
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

def generate_text(prompt):
    response = model.generate_content(prompt)
    generated_text = response._result.candidates[0].content.parts[0].text
    return generated_text

if __name__ == '__main__':
    app.run(debug=True)

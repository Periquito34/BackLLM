from flask import Flask, request, render_template
import google.generativeai as genai

app = Flask(__name__)


genai.configure(api_key="API_KEY")
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-questions', methods=['POST'])
def generate_questions():
    context = request.form['context']
    try:
        generated_text = generate_text(f"What kind of questions can I ask my client to better understand their needs? Context: {context}")
        questions = generated_text.split('\n')  
        print("Preguntas Generadas para Entender las Necesidades del Cliente:")  
        for question in questions:
            print(question)
        return render_template('questions.html', questions=questions)
    except Exception as e:
        error_message = f"Error durante la solicitud: {e}"
        return render_template('error.html', error=error_message)

def generate_text(prompt):
    response = model.generate_content(prompt)
    # Extraer el texto generado de la respuesta
    generated_text = response._result.candidates[0].content.parts[0].text
    return generated_text

if __name__ == '__main__':
    app.run(debug=True)

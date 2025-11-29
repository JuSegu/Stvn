import os
from flask import Flask, request, render_template_string
from dotenv import load_dotenv
from openai import OpenAI

# Cargar variables del .env
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<title>Chatbot Coca-Cola</title>
<h1>Chatbot Coca-Cola</h1>
<form method="POST">
    <textarea name="question" rows="4" cols="50" placeholder="Escribe tu pregunta..."></textarea><br>
    <button type="submit">Enviar</button>
</form>

{% if answer %}
<h2>Respuesta:</h2>
<p>{{ answer }}</p>
{% endif %}
"""

def obtener_respuesta(pregunta):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"Eres un experto en Coca-Cola. Responde claro y breve: {pregunta}"
    )
    return response.output_text

@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    if request.method == "POST":
        question = request.form.get("question")
        if question:
            answer = obtener_respuesta(question)
    return render_template_string(HTML_TEMPLATE, answer=answer)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, send_file
from flask_cors import CORS
import os
import subprocess
import uuid

app = Flask(__name__)
CORS(app)

@app.route("/generate", methods=["POST"])
def generate_resume():
    data = request.get_json()
    name = data.get("name", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    template_id = data.get("template", "template1")

    with open(f"templates/{template_id}.tex", "r") as f:
        template = f.read()

    filled = template.replace("{name}", name).replace("{email}", email).replace("{phone}", phone)

    uid = str(uuid.uuid4())
    tex_path = f"generated/{uid}.tex"
    pdf_path = f"generated/{uid}.pdf"

    with open(tex_path, "w") as f:
        f.write(filled)

    try:
        subprocess.run(["pdflatex", "-output-directory=generated", tex_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        return "Error generating PDF", 500

    return send_file(pdf_path, as_attachment=True)

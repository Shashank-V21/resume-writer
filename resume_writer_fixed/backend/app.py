from flask import Flask, request, send_file
from flask_cors import CORS
import os
import subprocess
import uuid

app = Flask(__name__)
CORS(app)

# Ensure the 'generated' folder exists
os.makedirs("generated", exist_ok=True)

@app.route("/")
def home():
    return "Resume Writer API is running!"

@app.route("/generate", methods=["POST"])
def generate_resume():
    data = request.get_json()

    # Extract user input
    name = data.get("name", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    template_id = data.get("template", "template1")

    # Template file path
    template_path = f"templates/{template_id}.tex"
    if not os.path.exists(template_path):
        return f"Template '{template_id}' not found.", 404

    # Read template content
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Replace placeholders
    filled = (
        template.replace("{name}", name)
                .replace("{email}", email)
                .replace("{phone}", phone)
    )

    # File paths
    uid = str(uuid.uuid4())
    tex_path = f"generated/{uid}.tex"
    pdf_path = f"generated/{uid}.pdf"

    # Write filled template to file
    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(filled)

    # Compile LaTeX to PDF
    try:
        subprocess.run(
            ["pdflatex", "-output-directory=generated", tex_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError as e:
        return f"Error generating PDF:\n{e.stderr.decode()}", 500

    # Send generated PDF
    return send_file(pdf_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)


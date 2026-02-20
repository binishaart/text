from flask import Flask, render_template, request, send_from_directory
import trimesh
import numpy as np
import os

app = Flask(__name__)
MODEL_DIR = "static/models"
os.makedirs(MODEL_DIR, exist_ok=True)

# Home page
@app.route("/", methods=["GET", "POST"])
def index():
    model_file = None
    if request.method == "POST":
        prompt = request.form.get("prompt", "")
        # Simple keyword-based 3D generator
        mesh = generate_3d_model(prompt)
        model_file = f"{MODEL_DIR}/model.glb"
        mesh.export(model_file)
    return render_template("index.html", model_file=model_file)

# Generate mesh from prompt (basic procedural example)
def generate_3d_model(prompt):
    prompt = prompt.lower()
    if "sphere" in prompt:
        mesh = trimesh.creation.icosphere(subdivisions=3, radius=1.0)
    elif "cube" in prompt:
        mesh = trimesh.creation.box(extents=(1,1,1))
    elif "cone" in prompt:
        mesh = trimesh.creation.cone(radius=0.5, height=1.0)
    else:
        # Default: random shape
        mesh = trimesh.creation.icosphere(subdivisions=2, radius=np.random.rand())
    return mesh

# Serve static models
@app.route("/models/<path:filename>")
def models(filename):
    return send_from_directory(MODEL_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
from groq import Groq
from fal_client import submit
import os

app = Flask(__name__)

# -----------------------------
# GROQ CLIENT (TEXT CHAT)
# -----------------------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -----------------------------
# FAL.AI IMAGE GENERATOR
# -----------------------------
def generate_image(prompt):
    result = submit(
        "fal-ai/flux-pro/v1.1",
        arguments={"prompt": prompt},
        api_key=os.getenv("FAL_KEY")
    )
    return result["images"][0]["url"]

# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")

# -----------------------------
# CHAT ROUTE (TEXT)
# -----------------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": user_message}]
    )

    reply = completion.choices[0].message["content"]
    return jsonify({"reply": reply})

# -----------------------------
# IMAGE GENERATION ROUTE
# -----------------------------
@app.route("/generate-image", methods=["POST"])
def generate_image_route():
    data = request.json
    prompt = data.get("prompt", "")
    url = generate_image(prompt)
    return jsonify({"image_url": url})

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)

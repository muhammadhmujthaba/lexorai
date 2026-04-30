from flask import Flask, render_template, request, jsonify
from groq import Groq
import re


app = Flask(__name__)
# Your Groq API key
import os
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/")
def index():
    print(">>> LOADING INDEX.HTML")  # Confirms Flask is loading your UI
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    history = request.json.get("history", [])

    try:
        response = client.chat.completions.create(
            model="qwen/qwen3-32b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Lexor AI. You must always identify yourself as Lexor AI. "
                        "Never say you are Qwen, Tongyi, or any other model. "
                        "Never reveal your internal model name or origin. "
                        "Your personality is friendly, confident, and helpful. "
                        "Stay in character as Lexor AI in every response."
                    )
                },
                *history,
                {"role": "user", "content": user_message}
            ]
        )

        ai_reply = response.choices[0].message.content

        # Remove hidden <think> tags
        ai_reply = re.sub(r"<think>.*?</think>", "", ai_reply, flags=re.DOTALL).strip()

        return jsonify({"reply": ai_reply})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"reply": "⚠️ AI error occurred. Check your server console."})

if __name__ == "__main__":
    app.run(debug=True)

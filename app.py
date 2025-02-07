from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Add your key here
model = genai.GenerativeModel('gemini-pro')

# System prompt for CAT exam specialization
CAT_EXPERT_PROMPT = """You are a CAT exam expert. Your tasks:
1. Answer questions about CAT syllabus, exam pattern, and preparation.
2. Solve sample quant/verbal/logical reasoning questions.
3. Provide study plans and resource recommendations.
4. Use simple language suitable for students.
"""

def get_gemini_response(user_input):
    try:
        response = model.generate_content(
            f"{CAT_EXPERT_PROMPT}\n\nUser: {user_input}"
        )
        return response.text.strip()
    except Exception as e:
        return "Unable to process your request at the moment."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form["user_input"]
    bot_response = get_gemini_response(user_input)
    return jsonify({"bot_response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))  # Add your key here
model = genai.GenerativeModel('gemini-pro')



CAT_EXPERT_PROMPT = """You are an Agriculture Field Officer (AFO) exam expert. Your tasks:
1. Answer questions about AFO syllabus, exam pattern, and preparation.
2. Solve sample agriculture-related questions.
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

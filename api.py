import os 
from flask import Flask, request, render_template, jsonify
import google.generativeai as genai 
from dotenv import load_dotenv 
import markdown 
 
load_dotenv() 
genai.configure(api_key=os.getenv("GEMINI_API_KEY")) 
 
model = genai.GenerativeModel("gemini-2.5-flash") 
 
app = Flask(__name__) 
 
@app.route("/", methods=["GET"])
def index(): 
    return render_template("index.html") 

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("prompt", "")
    base_prompt = """You are a helpful teacher named Chako. Who explains concepts in 
simple terms.  
Instead, you always respond with a question that guides the student to find the answer on 
their own but not for meta questions. use emojies and make it fun. 
{prompt} 
"""
    if prompt.strip():
        result = model.generate_content(base_prompt.format(prompt=prompt))
        response_html = markdown.markdown(result.text, extensions=["extra"])
        return jsonify({"response_html": response_html})
    return jsonify({"response_html": "Sorry, I didn't get that."})

@app.route("/hello", methods=["GET"]) 
def hello(): 
    return "Hello, World!" 
 
if __name__ == "__main__": 
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template
import requests
import json
import re
import random
import os

app = Flask(__name__, template_folder="../templates")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

fallback_ideas = [
    {
        "title": "Student Study Planner",
        "description": "A web app to plan daily study schedules",
        "whyItMatters": "Helps students stay organized",
        "coreFeatures": ["Task planner", "JavaScript", "Flask"],
        "techStack": ["Flask", "HTML", "CSS"],
        "bonus": "Dark mode"
    }
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generator():
    data = request.json
    time = data.get("time")
    skill = data.get("skill")
    category = data.get("category")

    prompt = f'''
    Generate a project idea.

    Time: {time}
    Skill: {skill}
    Category: {category}

    Return JSON:
    {{
      "title":"",
      "description":"",
      "whyItMatters":"",
      "coreFeatures":["","",""],
      "techStack":["","",""],
      "bonus":""
    }}
    '''

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
         print("KEY:", OPENROUTER_API_KEY)
         print("STATUS:", response.status_code)
         print("RESPONSE:", response.text)
        result = response.json()

        if "error" in result:
            return jsonify(random.choice(fallback_ideas))

        text = result["choices"][0]["message"]["content"]

        match = re.search(r'\{.*}', text, re.DOTALL)

        if match:
            return jsonify(json.loads(match.group()))
        else:
            return jsonify(random.choice(fallback_ideas))

    except Exception as e:
        print("error:", e)
        return jsonify(random.choice(fallback_ideas))


@app.route("/random")
def random_idea():
    return jsonify(random.choice(fallback_ideas))


def handler(request, *args, **kwargs):
    return app(request.environ, lambda *args: None)

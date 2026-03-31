from flask import Flask, request, jsonify, render_template
import requests
import json
import re
import random

app = Flask(__name__)

OPENROUTER_API_KEY = "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"

fallback_ideas = [
    {
        "title": "Student Study Planner",
        "description": "A web app to plan daily study schedules and track progress.",
        "whyItMatters": "Helps students stay organized and improve productivity.",
        "coreFeatures": ["Task planner", "Reminders", "Subject tracking"],
        "techStack": ["HTML", "JavaScript", "Flask"],
        "bonus": "Dark mode support"
    },
    {
        "title": "Food Waste Tracker",
        "description": "Track leftover food and reduce waste.",
        "whyItMatters": "Helps reduce food wastage and improve awareness.",
        "coreFeatures": ["Food logging", "Reports", "Notifications"],
        "techStack": ["Flask", "SQLite"],
        "bonus": "Charts for analytics"
    }
]

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    time = data.get("time")
    skill = data.get("skill")
    category = data.get("category")

    prompt = f"""
Generate a UNIQUE and DIFFERENT student project idea.

Time: {time}
Skill: {skill}
Category: {category}

Return ONLY JSON:
{{
"title":"",
"description":"",
"whyItMatters":"",
"coreFeatures":["","",""],
"techStack":["","",""],
"bonus":""
}}
"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3-8b-instruct",  # ✅ FIXED MODEL
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )

        result = response.json()

        print("API RESPONSE:", result) 
        if "error" in result:
            print("API ERROR:", result["error"])
            return jsonify(random.choice(fallback_ideas))

        text = result["choices"][0]["message"]["content"]

     
        match = re.search(r'\{.*\}', text, re.DOTALL)

        if match:
            return jsonify(json.loads(match.group()))
        else:
            print("JSON parse failed")
            return jsonify(random.choice(fallback_ideas))

    except Exception as e:
        print("ERROR:", e)
        return jsonify(random.choice(fallback_ideas))



@app.route("/random")
def random_idea():
    return jsonify(random.choice(fallback_ideas))


if __name__ == "__main__":
    app.run(debug=True)

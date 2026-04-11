from flask import Flask, request, jsonify, render_template
import requests, json, re, random, os

app = Flask(__name__, template_folder="templates")

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

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
    data = request.get_json(force=True, silent=True)

    if not data:
        return jsonify({"error": "No data received"}), 400

    time = data.get("time")
    skill = data.get("skill")
    category = data.get("category")
    if not time or not skill or not category:
     return jsonify({"error":"Missing fields"}),400
    
    if not OPENROUTER_API_KEY:
         return jsonify({"error": "API key not set"}), 500

    prompt = f"""
Generate a UNIQUE student project idea.

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
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        result = response.json()

        if "error" in result:
            return jsonify({"api_error": result}), 500

        if "choices" not in result:
            return jsonify({"unexpected_response": result}), 500

        text = result["choices"][0]["message"]["content"]

        try:
            return jsonify(json.loads(text))
        except:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return jsonify(json.loads(match.group()))
            else:
                return jsonify({"error": "JSON parse failed", "raw": text}), 500

    except Exception as e:
         return jsonify({"error": str(e)}), 500

@app.route("/random")
def random_idea():
    return jsonify(random.choice(fallback_ideas))

if __name__ == "__main__":
    app.run(debug=True)     

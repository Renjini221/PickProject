from flask import Flask, request, jsonify, render_template
import requests
import json
import re
import random
app = Flask(__name__, template_folder="../templates")

OPENROUTER_API_KEY ="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"

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
        return jsonify(random.choice(fafrom flask import Flask,request,jsonify,render_template
import requests
import json
import re
import random

app = Flask(__name__)
OPENROUTER_API_KEY="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"
fallback_ideas=[
{
    "title":"Student Study Planner",
    "Desciption":"A web app to plan daily study schedules and track progress",
    "WhyItMatters":"Helps students stay organized and improve productivity",
    "coreFeatures":["Task planner","javacript","Flask"],
    "bonus":"Dark moode"
},
{
    "title":"Food waste tracker",
    "description":"Tracks leftover food and reduce waste.",
    "whyItMatters":"Helps students stay organized nad improve productivity",
    "coreFeatures":["Task planner","remainders","Subject tracking"],
    "techStack":["Flask","SQLlite"],
    "bonus":"Charts fro analytics"
}
]
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate",methods=["POST"])
def generator():
    data = request.json
    time=data.get("time")
    skill = data.get("skill")
    category = data.get("category")

    prompt = f"""
    Generate a Unique and different student project idea

    Time:{time}
    Skill:{skill}
    category:{category}

    Return ONLY JSON
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
            "model": "openai/gpt-4o-mini",
            "messages": [{"role": "user", "content": prompt}]
        }
        )

        result = response.json()    
        print("API RESPONSE:", result)

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
    return app(request.environ, lambda *args: None)llback_ideas))


@app.route("/random")
def random_idea():
    return jsonify(random.choice(fallback_ideas))


def handler(request, *args, **kwargs):
    return app(request.environ, lambda *args: None)

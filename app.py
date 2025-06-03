from flask import Flask, render_template, request
import os
from parser import parse_resume
from flask import send_file
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["resume"]
        job_desc = request.form.get("job_desc")
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            data = parse_resume(file_path, job_desc)
            return render_template("result.html", data=data)
    return render_template("index.html")


@app.route("/download", methods=["GET"])
def download_excel():
    file_path = os.path.join("data", "parsed_data.xlsx")
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "No data available yet.", 404


@app.route("/graph")
def show_graph():
    excel_path = os.path.join("data", "parsed_data.xlsx")
    if not os.path.exists(excel_path):
        return "No parsed data available to generate graph.", 404

    df = pd.read_excel(excel_path)

    # Combine all skills from all rows
    all_skills = []
    for skill_list in df["Skills"].dropna():
        skills = [skill.strip() for skill in str(skill_list).split(',')]
        all_skills.extend(skills)

    # Count frequency
    from collections import Counter
    skill_counts = Counter(all_skills)
    top_skills = skill_counts.most_common(10)  # Top 10

    # Separate skills and values
    skills, counts = zip(*top_skills)

    # Plot bar chart
    plt.figure(figsize=(8, 5))
    plt.bar(skills, counts, color="skyblue")
    plt.title("Top 10 Skills from Parsed Resumes")
    plt.xlabel("Skills")
    plt.ylabel("Count")
    plt.xticks(rotation=30)
    plt.tight_layout()

    graph_path = os.path.join("static", "skill_distribution.png")
    plt.savefig(graph_path)
    plt.close()

    return render_template("graph.html", graph_url=graph_path)


if __name__ == "__main__":
    app.run(debug=True)

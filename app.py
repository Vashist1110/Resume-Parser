from flask import Flask, render_template, request
import os
from parser import parse_resume
from flask import send_file

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



if __name__ == "__main__":
    app.run(debug=True)

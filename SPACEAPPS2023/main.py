from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import envision

UPLOAD_FOLDER = "static"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/results")
def results():
    return render_template("results.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/live_demo", methods=["GET", "POST"])
def live_demo():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            dir = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(dir)
            envision.process(dir)
            return redirect(url_for("results", image=filename))

    return render_template("live_demo.html")

if __name__ == "__main__":
    app.run(debug=True)
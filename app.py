from flask import Flask, render_template, request, redirect, url_for
import tracker_script

app = Flask(__name__)

# Main home page route
@app.route("/")
def home():
    upcoming = tracker_script.get_upcoming_assignments()
    classes = tracker_script.get_classes()
    return render_template("home.html", assignments=upcoming, classes=classes)

# Route for adding classes
@app.route("/add-class", methods=["GET", "POST"])
def add_class():
    if request.method == "POST":
        class_name = request.form["class_name"]
        year = int(request.form["year"])
        term = int(request.form["term"])
        tracker_script.add_class(class_name, year, term)
        return redirect(url_for("home"))
    return render_template("add_class.html")

# Route for adding grades to a class
@app.route("/add-grade/<int:class_id>", methods=["GET", "POST"])
def add_grade(class_id):
    if request.method == "POST":
        assignment_name = request.form["assignment_name"]
        grade = float(request.form["grade"])
        weight = float(request.form["weight"])
        tracker_script.add_grade(class_id, assignment_name, grade, weight)
        return redirect(url_for("home"))
    return render_template("add_grade.html", class_id=class_id)

if __name__ == "__main__":
    tracker_script.initialize_database()
    app.run(debug=True)

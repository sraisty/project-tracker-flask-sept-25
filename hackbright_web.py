"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/")
def show_homepage():
    students = hackbright.get_all_student_names()
    projects = hackbright.get_all_project_titles()
    return render_template("homepage.html", projects=projects, students=students)

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get("github")

    first, last, github = hackbright.get_student_by_github(github)

    project_grade_list = hackbright.get_grades_by_github(github)

    return render_template("student_info.html", 
                           github=github, first=first, last=last,
                           grades_list = project_grade_list)


@app.route("/student-search")
def get_student_form():
    """ Show form for searching for a student
    """
    return render_template("student_search.html")

@app.route("/show-student-add")
def show_student_add_form():
    return render_template("add_student.html")

@app.route("/student-add", methods=['POST'])
def do_student_add():
    """ Add a student. """
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    github = request.form.get("github")

    hackbright.make_new_student(first_name, last_name, github)
    return render_template("user_added.html", first_name= first_name,
            last_name= last_name, github = github)

@app.route("/project")
def show_project_info():

    title = request.args.get("title")
    title, description, max_grade = hackbright.get_project_by_title(title)

    new_list = []
    student_grades_list = hackbright.get_grades_by_title(title)
    for github, grade in student_grades_list:
        first, last, github = hackbright.get_student_by_github(github)
        new_list.append([first, last, grade, github])


    return render_template("project_info.html",
                            title=title,
                            description=description,
                            max_grade=max_grade,
                            student_grades_list = new_list)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)

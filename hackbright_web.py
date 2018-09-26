"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/")
def show_homepage():
    students = hackbright.get_all_students()
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


@app.route("/student-add")
def show_student_add_form():
    return render_template("add_student.html")


@app.route("/do-student-add", methods=['POST'])
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


@app.route("/project-add")
def show_project_add_form():
    return render_template("add_project.html")

@app.route("/do-project-add", methods=['POST'])
def do_project_add():
    title = request.form.get("title")
    description = request.form.get("description")
    max_grade = request.form.get("max-grade")

    hackbright.make_new_project(title, description, max_grade)
    return render_template("thank_add_project.html", title=title)


@app.route("/grade-assign")
def show_grade_assign():
    students = hackbright.get_all_students()
    project_titles = hackbright.get_all_project_titles()
    return render_template("assign_grade.html", project_titles=project_titles, students=students)

@app.route("/do-grade-assign", methods=['POST'])
def do_grade_assign():
    github = request.form.get('github')
    title = request.form.get('title')
    grade = request.form.get('grade')

    # Check to see if this students project has already been graded.
    # None is returned if this grade doesn't exist yet
    old_grade = hackbright.get_grade_by_github_title(github, title)
    if old_grade:
        hackbright.update_grade(github, title, grade)
    else:
        # student's project has NOT been graded yet, so insert into the DB
        hackbright.assign_grade(github, title, grade)

    return render_template("thank-assign-grade.html")

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)

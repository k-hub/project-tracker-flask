from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    projects_grades = hackbright.get_grades_by_github(github)
    html = render_template("student_info.html",
                            first=first,
                            last=last,
                            github=github,
                            projects_grades=projects_grades)

    return html

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/new-student")
def add_student():
    """Show form for adding a new student."""

    return render_template("new_student.html")


@app.route("/student-add", methods=['POST'])
def confirmation():
    """Confirm student successfully added."""

    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    github = request.form.get('github')

    hackbright.make_new_student(firstname, lastname, github)

    return render_template("student_add_confirmation.html", firstname=firstname,
                                                            lastname=lastname,
                                                            github=github)

@app.route("/project/<title>")
def project(title):
    """Show project title, description and maximum grade."""

    title, description, maximum_grade = hackbright.get_project_by_title(title)

    return render_template("project_info.html", title=title,
                                                description=description,
                                                maximum_grade=maximum_grade)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)

from flask import Flask
from flask import (
    render_template, session,
    request, url_for, redirect
)

app = Flask(__name__)
app.secret_key = 'the random string'

def question_1():
    question = "Commercial or Residential?"
    return (
        f"""
        <form method="POST">
        <p>{question}</p>
        <input type="radio" name="question" value="Commercial">Commercial<br>
        <input type="radio" name="question" value="Residential" checked>Residential<br>
        <input type="submit" value="Submit">
        </form>
        """,
        question
    )

def question_2():
    question = "What building materials are being considered?"
    return (
        f"""
        <form method="POST">
        <p>{question}</p>
        <input type="checkbox" id="wood" name="question" value="wood">
        <label for="wood"> wood</label><br>
        <input type="checkbox" id="granite" name="question" value="granite">
        <label for="granite"> Granite</label><br>
        <input type="checkbox" id="terracotta" name="question" value="terracotta">
        <label for="terracotta"> Terracotta</label><br><br>
        <input type="checkbox" id="steel" name="question" value="steel">
        <label for="steel"> Steel</label><br><br>
        <input type="submit" value="Submit">
        </form>
        """,
        question
    )

def construct_answer(questions, answers):
    codes = []
    print(questions)
    questions = list(set(questions))
    for index, question in enumerate(questions):
        if question == "Commercial or Residential?":
            if answers[index] == "Residential":
                codes.append('1')
            else:
                codes.append('2')
        if question == "What building materials are being considered?":
            if "wood" in answers[index]:
                codes.append("3")
            if "granite" in answers[index]:
                codes.append("4")
            if "terracotta" in answers[index]:
                codes.append("5")
            if "steel" in answers[index]:
                codes.append("6")
    building_codes = ",".join(codes)
    return f"""
    <p>You should consider building codes {building_codes}</p>
    """

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get("question_number"):
        session["question_number"] = 1
    if not session.get("questions"):
        session["questions"] = []
    if not session.get("answers"):
        session["answers"] = []

    if request.method == 'POST':
        if session["question_number"] == 2:
            session["answers"].append(request.form.getlist('question'))
        else:
            session["answers"].append(request.form['question'])
        session["question_number"] += 1

        print(session["question_number"])
        if session["question_number"] == 3:
            result = construct_answer(session["questions"], session["answers"])
            return render_template("index.html", result=result)
        elif session["question_number"] == 2:
            form_template, question = question_2()
            session["questions"].append(question)
            return render_template("index.html", form_template=form_template)

    form_template, question = question_1()
    session["questions"].append(question)
    return render_template("index.html", form_template=form_template)
    
@app.route("/reset", methods=["GET", "POST"])
def reset():
    session["question_number"] = 1
    session["questions"] = []
    session["answers"] = []
    
    return """
    <html>
    <p>state reset</p>
    </html>
    """

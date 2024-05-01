from flask import Flask, render_template, request, redirect, session
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
#Needs password below
conn_str = "mysql://root:localUnkers1!@localhost/160finaldb"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


@app.route("/")
def get_index():
    return render_template("index.html", loggedin=session.get("username"), success=None)


@app.route("/login", methods=["GET"])
def get_login_template():
    session["username"] = None
    session["acct_type"] = None
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    try:
        user = conn.execute(
            text(f"SELECT username FROM accounts WHERE password = :password AND username = :email_or_username OR email = :email_or_username"),
            request.form
        )
        user = "".join(user.first())
        session["username"] = user
        acct_type = conn.execute(
            text(f"SELECT acct_type FROM accounts WHERE username = '{session.get('username')}'")).first()
        acct_type = "".join(acct_type)
        session["acct_type"] = acct_type
        return redirect("/")
    except Exception as e:
        error = e.orig.args[1]
        print(error)
        return render_template("login.html", error=error)


@app.route("/logout", methods=["GET"])
def logout():
    session["username"] = None
    session["acct_type"] = None
    return redirect("/")


@app.route("/register", methods=["GET"])
def get_register_template():
    session["username"] = None
    session["acct_type"] = None
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    if request.form.get("password") == request.form.get("password-confirm"):
        try:
            conn.execute(
                text(f"INSERT INTO accounts (email, username, password, acct_type) VALUES (:email, :username, :password, :radio)"),
                request.form
            )
            conn.commit()
            session["username"] = request.form.get("username")
            session["acct_type"] = request.form.get("radio")
            return render_template("register.html", error=None, success="Account created successfully!", loggedin=session.get("username"))
        except Exception as e:
            error = e.orig.args[1]
            print(error)
            return render_template("register.html", error=error, succes=None)
    else:
        return render_template("register.html", error="Passwords do not match", success=None)


@app.route("/tests", methods=["GET"])
def get_test_taking_template():
    if session.get("username"):
        acct_type = conn.execute(text(f"SELECT acct_type FROM accounts WHERE username = '{session.get('username')}'")).first()
        acct_type = "".join(acct_type)
    else:
        acct_type = None
    tests = conn.execute(text("SELECT * FROM tests"))
    return render_template("test_list.html", loggedin=session.get("username"), tests=tests, acct_type=session.get("acct_type"))


@app.route("/tests/<test>")
def take_test(test):
    questions = conn.execute(text(f"SELECT question FROM test_questions WHERE test_name = {test}"))
    return render_template("testing.html", test=test, questions=questions, loggedin=session.get("username"), acct_type=session.get("acct_type"))


@app.route("/manage_tests", methods=["GET"])
def get_manage_tests_template():
    tests = conn.execute(text("SELECT * FROM tests"))
    return render_template("manage_tests.html", loggedin=session.get("username"), acct_type=session.get("acct_type"), tests=tests, success=None)


@app.route("/update_tests/<test>", methods=["GET"])
def get_update_test_template(test):
    return render_template("update.html", loggedin=session.get("username"), acct_type=session.get("acct_type"), test=test)


@app.route("/create_new_test", methods=["GET"])
def get_creation_template():
    return render_template("create_test.html", error=None, acct_type=session.get("acct_type"), loggedin=session.get("username"))


@app.route("/create_new_test", methods=["POST"])
def create_test():
    try:
        conn.execute(
            text(f"INSERT INTO tests (created_by, test_name, date_created, num_questions) "
                 f"VALUES ('{session.get("username")}', '{request.form.get("test_name")}',"
                 f" CURDATE(), {int(request.form.get('num_questions'))})"))
        for i in range(0, int(request.form.get("num_questions"))):
            conn.execute(text(f"INSERT INTO test_questions (question, test_name)"
                              f"VALUES ('{request.form.get(f'question-{i + 1}')}', '{request.form.get("test_name")}')"))
        conn.commit()
        return render_template("index.html", loggedin=session.get("username"), success="Test created successfully!")
    except Exception as e:
        error = e.orig.args[1]
        print(error)
        return render_template("create_test.html", error=error)


if __name__ == "__main__":
    app.run(debug=True)

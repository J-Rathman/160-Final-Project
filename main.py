from flask import Flask, render_template, request, redirect, session
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
#Needs password below
conn_str = "mysql://root:PASSWORD@localhost/160finaldb"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


@app.route("/")
def get_index():
    return render_template("index.html", loggedin=session.get("username"))


@app.route("/login", methods=["GET"])
def get_login_template():
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
        return redirect("/")
    except Exception as e:
        error = e.orig.args[1]
        print(error)
        return render_template("login.html", error=error)


@app.route("/logout", methods=["GET"])
def logout():
    session["username"] = None
    return redirect("/")


@app.route("/register", methods=["GET"])
def get_register_template():
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
            return render_template("register.html", error=None, success="Account created successfully!", loggedin=session.get("username"))
        except Exception as e:
            error = e.orig.args[1]
            print(error)
            return render_template("register.html", error=error, succes=None)
    else:
        return render_template("register.html", error="Passwords do not match", success=None)


@app.route("/take_a_test", methods=["GET"])
def get_test_taking_template():
    return render_template("take_test.html", loggedin=session.get("username"))


@app.route("/manage_tests", methods=["GET"])
def get_manage_tests_template():
    return render_template("manage_tests.html", loggedin=session.get("username"))


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text

app = Flask(__name__)
#Needs password below
#conn_str = "mysql://root:password@localhost/160finaldb"
#engine = create_engine(conn_str, echo=True)
#conn = engine.connect()


@app.route("/")
def get_index():
    return render_template("index.html")


@app.route("/login", methods=["GET"])
def get_login_template():
    return render_template("accounts.html")


@app.route("/register", methods=["GET"])
def get_register_template():
    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register():
    if request.form.get("password") == request.form.get("password-confirm"):
        try:
            conn.execute(
                #text(f"INSERT INTO accountsxp (email, username, password) VALUES (:email, :username, :password)"),
                #request.form
            )
            conn.commit()
            return render_template("register.html", error=None, success="Account created! Click <a href='/login'>here</a> to login.")
        except Exception as e:
            error = e.orig.args[1]
            print(error)
            return render_template("register.html", error=error, success=None)
    else:
        return render_template("register.html", error="Passwords do not match", success=None)


@app.route("/take_a_test", methods=["GET"])
def get_test_taking_template():
    return render_template("take_test.html")


@app.route("/manage_tests", methods=["GET"])
def get_manage_tests_template():
    return render_template("manage_tests.html")


if __name__ == '__main__':
    app.run(debug=True)

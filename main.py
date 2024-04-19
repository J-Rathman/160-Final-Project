from flask import Flask, render_template, request
from sqlalchemy import Column, Integer, String, Numeric, create_engine, text

app = Flask(__name__)
#Needs password below
#conn_str = "mysql://root:PASSWORD@localhost/160finaldb"
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


@app.route("/take_a_test", methods=["GET"])
def get_test_taking_template():
    return render_template("take_test.html")


@app.route("/manage_tests", methods=["GET"])
def get_manage_tests_template():
    return render_template("manage_tests.html")


if __name__ == '__main__':
    app.run(debug=True)

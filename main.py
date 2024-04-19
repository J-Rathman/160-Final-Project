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


if __name__ == '__main__':
    app.run(debug=True)

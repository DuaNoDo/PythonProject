from flask import request
from flask import Flask

app=Flask(__name__)

app.debug=True

@app.route("/hello")

def hello():
    name=request.args.get("name")
    return "hello {}".format(name)


if __name__=="__main__":
    app.run()


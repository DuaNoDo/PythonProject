from flask import Flask

app=Flask(__name__)

app.debug=True

@app.route("/hello/<name>")

def hello(name):
    return "hello {}".format(name)


if __name__=="__main__":
    app.run()



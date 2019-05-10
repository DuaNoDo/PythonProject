from flask import Flask
from flask import send_from_directory
app=Flask(__name__,static_url_path="/static")

app.debug=True

@app.route('/<path:path>')
def serve_page(path):
    return send_from_directory('static',path)

@app.route("/")
def hello():
    return "hello Python"


if __name__=="__main__":
    app.run()



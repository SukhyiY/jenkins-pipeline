from flask import Flask, render_template
import os
app = Flask(__name__)

@app.route('/')
def hello():
    image_tag = os.environ.get('app-version')
    return render_template('index.html', image_tag=image_tag)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)

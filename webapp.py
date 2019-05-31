from flask import Flask, render_template, image
import os
app = Flask(__name__)

@app.route('/')
def hello():
    image_tag = os.environ.get('app_version')
    return render_template('index.html', image_tag=image_tag)
    return image('Flask-logo.png')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)

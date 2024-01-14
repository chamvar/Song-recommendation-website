# "https://www.youtube.com/watch?v=HE9NvGe9bpI"

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    youtube_url = request.form['youtube_url']
    return render_template('index.html', youtube_url=youtube_url, playing=True)

if __name__ == '__main__':
    app.run(debug=True)

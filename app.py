from flask import Flask, render_template, redirect, url_for

# Initialize Flask app
app = Flask(__name__)

# Counter for the buttons
counter = {"yes": 0, "no": 0}

@app.route('/')
def index():
    return render_template('index.html', yes_count=counter["yes"], no_count=counter["no"])

@app.route('/vote/<vote>', methods=['POST'])
def vote(vote):
    if vote in counter:
        counter[vote] += 1
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    counter["yes"] = 0
    counter["no"] = 0
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

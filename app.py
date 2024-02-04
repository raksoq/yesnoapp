from flask import Flask, render_template, redirect, url_for
import redis

app = Flask(__name__)

# Initialize Redis
redis_url = "redis://redis:6379/0"
r = redis.Redis.from_url(redis_url)

def check_redis_connection():
    try:
        r.ping()
        return "Yes"
    except (redis.ConnectionError, redis.TimeoutError):
        return "No"

@app.route('/')
def index():
    yes_count = r.get('yes') or 0
    no_count = r.get('no') or 0
    # Convert to int since Redis stores everything as strings
    yes_count = int(yes_count)
    no_count = int(no_count)
    redis_connected = check_redis_connection()  # Check connection status
    return render_template('index.html', yes_count=yes_count, no_count=no_count, redis_connected=redis_connected)

@app.route('/vote/<vote>', methods=['POST'])
def vote(vote):
    if vote in ["yes", "no"] and check_redis_connection() == "Yes":
        r.incr(vote)
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    if check_redis_connection() == "Yes":
        r.set('yes', 0)
        r.set('no', 0)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

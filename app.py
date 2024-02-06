from flask import Flask, render_template, redirect, url_for, request
import redis

app = Flask(__name__)

# Initialize Redis
redis_url = "redis://yesnoapp-redis-master:6379/0"
try:
    r = redis.Redis.from_url(redis_url)
    r.ping()  # Attempt to connect to Redis.
    redis_connected = "Yes"
except (redis.ConnectionError, redis.TimeoutError):
    r = None  # If Redis is not connected, set r to None.
    redis_connected = "No"

def get_vote_counts():
    """Safely get vote counts from Redis, returning 0 if not connected or on error."""
    if r:
        try:
            yes_count = int(r.get('yes') or 0)
            no_count = int(r.get('no') or 0)
            return yes_count, no_count
        except redis.RedisError:
            pass  # Optionally log this error.
    return 0, 0  # Default values if Redis is not connected or on error.

@app.route('/')
def index():
    yes_count, no_count = get_vote_counts()
    return render_template('index.html', yes_count=yes_count, no_count=no_count, redis_connected=redis_connected)

@app.route('/vote/<vote>', methods=['POST'])
def vote(vote):
    if vote in ["yes", "no"] and redis_connected == "Yes":
        try:
            r.incr(vote)
        except redis.RedisError:
            pass  # Optionally log this error or handle it.
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset():
    if redis_connected == "Yes":
        try:
            r.set('yes', 0)
            r.set('no', 0)
        except redis.RedisError:
            pass  # Handle error, maybe log it.
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

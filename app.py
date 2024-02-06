from flask import Flask, render_template, redirect, url_for, request
import redis
import time

app = Flask(__name__)

# Function to wait for Redis to be ready
def wait_for_redis(redis_url, max_attempts=10, delay=2):
    attempts = 0
    while attempts < max_attempts:
        try:
            r = redis.Redis.from_url(redis_url)
            r.ping()  # Attempt to connect to Redis.
            print("Connected to Redis")
            return r  # Redis is ready, return the connection.
        except (redis.ConnectionError, redis.TimeoutError) as e:
            print(f"Waiting for Redis... ({e})")
            time.sleep(delay)  # Wait before retrying
            attempts += 1
    print("Failed to connect to Redis after several attempts.")
    return None

# Initialize Redis with a wait-for-ready loop
redis_url = "redis://yesnoapp-redis-master:6379/0"
r = wait_for_redis(redis_url)
redis_connected = "Yes" if r else "No"

def get_vote_counts():
    """Safely get vote counts from Redis, returning 0 if not connected or on error."""
    if r:
        try:
            yes_count = int(r.get('yes') or 0)
            no_count = int(r.get('no') or 0)
            return yes_count, no_count
        except redis.RedisError as e:
            print(f"Error retrieving vote counts from Redis: {e}")  # Optionally log this error.
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
        except redis.RedisError as e:
            print(f"Failed to increment vote for '{vote}': {e}")  # Optionally log this error or handle it.
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset():
    if redis_connected == "Yes":
        try:
            r.set('yes', 0)
            r.set('no', 0)
        except redis.RedisError as e:
            print(f"Failed to reset vote counts: {e}")  # Handle error, maybe log it.
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

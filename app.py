from flask import Flask, render_template, redirect, url_for, request
import redis
import time
import os

app = Flask(__name__)

# Function to construct the Redis URL from environment variables
def get_redis_url():
    host = os.getenv('REDIS_HOST', 'yesnoapp-redis-master')
    port = os.getenv('REDIS_PORT', '6379')
    password = os.getenv('REDIS_PASSWORD', None)
    if password:
        return f"redis://:{password}@{host}:{port}/0"
    else:
        return f"redis://{host}:{port}/0"

# Function to wait for Redis to be ready
def wait_for_redis(redis_url, max_attempts=15, delay=2):
    """Attempt to connect to Redis with a retry loop."""
    for attempt in range(max_attempts):
        try:
            r = redis.Redis.from_url(redis_url)
            r.ping()  # Attempt to connect to Redis.
            print("Connected to Redis")
            return r, "Yes"
        except (redis.ConnectionError, redis.TimeoutError) as e:
            print(f"Waiting for Redis... Attempt {attempt+1}/{max_attempts}: {e}")
            time.sleep(delay)
    print("Failed to connect to Redis after several attempts.")
    return None, "No"

# Initialize Redis with a wait-for-ready loop using the constructed URL
redis_url = get_redis_url()
r, redis_connected = wait_for_redis(redis_url)

# Read the environment variable for the application environment
environment = os.getenv('ENV', 'development')  # Default to 'development' if not set

def get_vote_counts():
    """Safely get vote counts from Redis, returning 0 if not connected or on error."""
    if r is not None:
        try:
            yes_count = int(r.get('yes') or 0)
            no_count = int(r.get('no') or 0)
            return yes_count, no_count
        except redis.RedisError:
            print("Error retrieving vote counts from Redis.")
    return 0, 0

@app.route('/')
def index():
    yes_count, no_count = get_vote_counts()
    return render_template('index.html', yes_count=yes_count, no_count=no_count, redis_connected=redis_connected, environment=environment)

@app.route('/vote/<vote>', methods=['POST'])
def vote(vote):
    if vote in ["yes", "no"] and redis_connected == "Yes" and r is not None:
        try:
            r.incr(vote)
        except redis.RedisError:
            print(f"Error incrementing vote for '{vote}'.")
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset():
    if redis_connected == "Yes" and r is not None:
        try:
            r.set('yes', 0)
            r.set('no', 0)
        except redis.RedisError:
            print("Error resetting vote counts.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

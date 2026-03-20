import redis
import time

redis_client = redis.Redis(host="localhost", port=6379, db=1) # Separate DB for rate limiting

def is_rate_limited(user_id, limit=5, window=60): # 5 requests per minute (Fixed limit and window for simplicity)
    """
    limit = max requests
    window = time in seconds
    """
    key = f"rate_limit:user:{user_id}" # Key format: rate_limit:user:<user_id

    current = redis_client.get(key) # Get current count

    if current and int(current) >= limit: # If limit exceeded, return True
        return True

    pipe = redis_client.pipeline() # Use pipeline for atomic increment and expiry
    pipe.incr(key, 1) # Increment count

    # set expiry only first time
    if not current:
        pipe.expire(key, window)
    pipe.execute() # Execute pipeline
    return False 
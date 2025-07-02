import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify

# Define a secret key used for encoding and decoding JWT tokens
SECRET_KEY = "egyptian_key"

# Function to encode a JWT token for a given user ID
def encode_token(customer_id):
    # Create the payload for the JWT token
    payload = {
        # Set the expiration time for the token (1 hour from now)
        "exp": datetime.now(timezone.utc) + timedelta(days=0, hours=1),
        # Set the issued-at time for the token (current time)
        "iat": datetime.now(timezone.utc),
        # Set the subject of the token (user ID)
        "sub": str(customer_id)
    }

    # Encode the payload into a JWT token using the secret key and HS256 algorithm
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token  # Return the encoded token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            bearer = request.headers["Authorization"]
            print(f"Authorization header: {bearer}")
            if bearer.startswith("Bearer "):
                token = bearer.split(" ")[1]
        
        if not token:
            print("❌ No token provided.")
            return jsonify({"message": "Token is missing!"}), 401

        try:
            print("Decoding token:", token)
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            print("✅ Decoded data:", data)
            customer_id = int(data["sub"])
        except jwt.ExpiredSignatureError:
            print("❌ Token expired.")
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError as e:
            print(f"❌ Invalid token: {e}")
            return jsonify({"message": "Invalid token!"}), 401

        return f(customer_id, *args, **kwargs)
    return decorated


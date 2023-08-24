import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import datetime
import pytz  # Import the pytz library

# Load encrypted private key from file
with open('jwtRS256.key', 'rb') as private_key_file:
    encrypted_private_key = private_key_file.read()

passphrase = b'qwertyuiop'  # Passphrase as bytes

# Decrypt the private key
private_key = load_pem_private_key(
    encrypted_private_key,
    password=passphrase,
)

# Load public key from file
with open('jwtRS256.key.pub', 'rb') as public_key_file:
    public_key = public_key_file.read()

# Get the current UTC time
current_time_utc = datetime.datetime.now(pytz.utc)

# Define a longer expiration time (e.g., 7 days from now)
expiration_time = current_time_utc + datetime.timedelta(days=7)
exp_timestamp = int(expiration_time.timestamp())

# Payload to be included in the JWT
payload = {
    'sub': '1234567890',  # Subject
    'name': 'John Doe',
    'iat': int(current_time_utc.timestamp()) - 10,  # Adjust for potential clock skew
    'exp': exp_timestamp  # Expiration (Unix timestamp)
}

# Create the JWT token using the decrypted private key
token = jwt.encode(payload, private_key, algorithm='RS256', headers={"kid": "jwtRS256.key"})

print("Generated JWT Token:")
print(token)

# Verify the token using the public key
try:
    decoded_payload = jwt.decode(token, public_key, algorithms=['RS256'])
    print("Decoded Payload:")
    print(decoded_payload)
except jwt.ExpiredSignatureError:
    print("Token has expired.")
except jwt.InvalidTokenError:
    print("Token verification failed.")

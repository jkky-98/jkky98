import base64
import os

# Get a number that is random enough for cryptographic purposes.
print(base64.b64encode(os.urandom(50)).decode('ascii'))

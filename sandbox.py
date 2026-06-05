import hashlib as hl

key = "usr"
binary = key.encode() # Encode the password to bytes
hash = hl.sha256(binary) # Hash the password using SHA-256
hashHex = hash.hexdigest() # Convert the hash to hexadecimal format
print(hashHex)
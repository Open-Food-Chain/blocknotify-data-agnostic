from komodo_py.wallet import WalletInterface
from komodo_py.explorer import Explorer

import os
import hashlib
import ecdsa
from dotenv import load_dotenv

load_dotenv()

seed = os.getenv('SEED')

def encode_base58(input_data):
	ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

	# Check if input_data is a hex string and convert to byte buffer if necessary
	if isinstance(input_data, str):
		# Convert hex string to byte buffer
		buffer = bytes.fromhex(input_data)
	elif isinstance(input_data, bytes):
		buffer = input_data
	else:
		raise TypeError("Input must be a hex string or bytes")

	# Convert the buffer to a list of integers for easier processing
	digits = [0]
	for byte in buffer:
		carry = byte
		for i in range(len(digits)):
			carry += digits[i] << 8
			digits[i] = carry % 58
			carry //= 58
		while carry > 0:
			digits.append(carry % 58)
			carry //= 58

	# Count leading zeros in buffer
	zero_count = 0
	for byte in buffer:
		if byte == 0:
			zero_count += 1
		else:
			break

	# Convert digits to Base58 string
	encoded = ''.join(ALPHABET[d] for d in reversed(digits))

	# Add leading zeros
	return ALPHABET[0] * zero_count + encoded

def get_wallet_address(self, walletstring):
	if (WalletManager.is_hex_string(string) and len(string) > 15):
		string = WalletManager.hexstring_to_bytearray(string)
	else:
		string = string.encode('utf-8')

	sig = self.sign_key.sign_digest_deterministic(string, hashfunc=hashlib.sha256, sigencode = ecdsa.util.sigencode_der_canonize)
	return sig

def hexstring_to_bytearray(hexstring):
	# Remove '-' characters from the hex string
	hexstring = hexstring.replace('-', '')
	print(hexstring)
	try:
		# Convert the cleaned hex string to bytes
		byte_array = bytes.fromhex(hexstring)
		return byte_array
	except ValueError:
		# Handle invalid hex input
		return None

#seed = "org_dimitra"

explorer_url = os.getenv('EXPLORER_URL')

explorer = Explorer(explorer_url)

wal_in = WalletInterface(explorer, seed, True)

#sign_key = wal_in.get_sign_key()

#unique = "862bab48-5f51-4496-b959-d2fe60ea5442"

#unique = hashlib.sha256(unique.encode()).hexdigest()

#unique = hexstring_to_bytearray(unique)
		
#unique = sign_key.sign_digest_deterministic(unique, hashfunc=hashlib.sha256, sigencode = ecdsa.util.sigencode_der_canonize)
		
#unique = encode_base58(unique)

#explorer_url = os.getenv('EXPLORER_URL')

#explorer = Explorer(explorer_url)

#wal_in = WalletInterface(explorer, unique, True)

print("get addy")
print(wal_in.get_address())
print("get pub key")
print(wal_in.get_public_key())
print("get wif")
print(wal_in.get_wif())

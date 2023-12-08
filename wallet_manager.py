from komodo_py.transaction import TxInterface
from komodo_py.explorer import Explorer
from komodo_py.wallet import WalletInterface
from ecpy.curves     import Curve,Point
import hashlib
import ecdsa

class WalletManager:
	def __init__(self, org_wal, batch_obj, keys_to_remove):
		self.org_wal = org_wal 
		self.batch_obj = batch_obj
		self.sign_key = org_wal.get_sign_key()
		self.clean_batch_obj = self.remove_keys_from_json_object(keys_to_remove)
		self.key_wallets = self.get_wallets()

	def get_wallet_address(self, string):
		string = string.encode('utf-8')
		sig = self.sign_key.sign_digest_deterministic(string, hashfunc=hashlib.sha256, sigencode = ecdsa.util.sigencode_der_canonize)
		return sig

	def encode_base58(self, buffer):
		ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

		# Convert the buffer to a list of integers for easier processing
		digits = [0]
		for byte in buffer:
			carry = byte
			for j in range(len(digits)):
				carry += digits[j] << 8
				digits[j] = carry % 58
				carry //= 58
			while carry > 0:
				digits.append(carry % 58)
				carry //= 58

	    # Remove leading zeros
		zero_count = 0
		for byte in buffer:
			if byte == 0:
				zero_count += 1
			else:
				break

		# Convert digits to Base58 string
		return ALPHABET[digits.pop()] + ALPHABET[0] * zero_count + ''.join(ALPHABET[d] for d in reversed(digits))

	def get_wallets(self):
		name_and_wal = {}

		for key in self.clean_batch_obj:
			new_seed = self.encode_base58(self.get_wallet_address(key))
			new_wallet = WalletInterface("https://ofcmvp.explorer.batch.events/", new_seed)
			name_and_wal[key] = new_wallet

		return name_and_wal

	def remove_keys_from_json_object(self, keys_to_remove):
		new_obj = self.batch_obj.copy()  # Create a shallow copy of the original dictionary
		for key in keys_to_remove:
			new_obj.pop(key, None)  # Remove the key if it exists
		return new_obj


	def create_batch_address(self, batch_value ):
		new_seed = self.encode_base58(self.get_wallet_address(batch_value))
		new_wallet = WalletInterface("https://ofcmvp.explorer.batch.events/", new_seed)
		return new_wallet.get_address()

	def fund_offline_wallets(self):
		to_addrs = []
		amounts  = [] 

		for key in self.key_wallets:
			if ( len(self.key_wallets[key].get_utxos()) < 10):
				to_addrs.append(self.key_wallets[key].get_address())
				amounts.append(100)


		if (len(to_addrs) != 0):
			txid = self.org_wal.send_tx_force(to_addrs, amounts)["txid"]
			return txid

		return "fully funded"

	def send_batch_transaction(self, tx_obj, batch_value):
		to_addr = self.create_batch_address(batch_value)
		tx_ids = {}

		for key in self.key_wallets:
			send_addrs = []
			send_amounts = []
			
			try:
				send_amounts = tx_obj[key]
			except ValueError:
				print("obj not complete")
				return "obj not complete"

			for i in range(len(send_amounts)):
				send_addrs.append(to_addr)

			txid = self.key_wallets[key].send_tx_force(send_addrs, send_amounts)	
			tx_ids[key] = txid

		return tx_ids



class WalManInterface:
	def __init__(self, org_wal, batch_obj, keys_to_remove):
		self.wallet_manager = WalletManager(org_wal, batch_obj, keys_to_remove)

	def fund_offline_wallets(self):
		return self.wallet_manager.fund_offline_wallets()

	def send_batch_transaction(self, tx_obj, batch_value):
		return self.wallet_manager.send_batch_transaction(tx_obj, batch_value)
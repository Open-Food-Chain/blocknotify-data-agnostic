import re
import json
import binascii
import hashlib
from datetime import datetime

from blocknotify.wallet_manager import WalletManager

class ObjectParser:

    def dubble_hash(self, string):
    	ret = self.hash_value(string)
    	ret = self.hash_value(ret)

    	return ret

    def hash_value(self, string):
    	# Encode the string into bytes
    	encoded_string = string.encode()

    	# Create a new SHA256 hash object
    	sha256_hash = hashlib.sha256()

    	# Update the hash object with the bytes of the string
    	sha256_hash.update(encoded_string)

    	# Return the hexadecimal representation of the digest
    	return sha256_hash.hexdigest()

    def find_and_do(self, obj, key, func):
    	if key in obj:
    		if isinstance(obj[key], dict):
    			self.find_and_do(obj[key], key, func)
    		obj[key]["value"] = func(obj[key]["value"])

    	return obj

    def value_is_value(self, obj):
    	"""
    	Transforms a JSON-like object by replacing any dictionary with a 'value' key by its value.

    	Args:
    	obj (dict or list): The JSON-like object to transform.

    	Returns:
    	The transformed object.
    	"""

    	if isinstance(obj, dict):
    		for key in obj:
    			# If the value is a dict or list, recurse into it
    			if isinstance(obj[key], (dict, list)):
    				# Replace dict containing 'value' key with its value
    				if "value" in obj[key]:
    					obj[key] = obj[key]["value"]
    				else:
    					obj[key] = self.value_is_value(obj[key])
    			# Otherwise, apply the function to the value
    			else:
    				obj[key] = self.value_is_value(obj[key])
    	elif isinstance(obj, list):
    		for index, item in enumerate(obj):
    			# If the item is a dict or list, recurse into it
    			if isinstance(item, (dict, list)):
    				# Replace dict containing 'value' key with its value
    				if isinstance(item, dict) and "value" in item:
    					obj[index] = item["value"]
    				else:
    					obj[index] = self.value_is_value(item)
    			# Otherwise, apply the function to the item
    			else:
    				obj[index] = self.value_is_value(item)

    	return obj

    def walk_and_apply(self, obj, target_attribute, operation):
    	"""
    	Recursively walks through a JSON object and applies the given operation
    	to the 'value' attribute of every object that contains the target attribute.

    	Args:
    	obj (dict or list): The JSON object to walk through.
    	target_attribute (str): The name of the attribute to look for.
    	operation (function): The operation to apply to the 'value' attribute.

    	Returns:
    	None: The function modifies the object in place.
    	"""

    	# If the object is a dictionary
    	if isinstance(obj, dict):
    		for key, value in obj.items():
    			print(key)
    			# Check if this dictionary contains the target attribute
    			if key == target_attribute:
    				if value == True:
    					#print(key)
    					obj['value'] = operation(obj['value'])
    			# Otherwise, if the value is a dictionary or list, recurse into it
    			else:
    				self.walk_and_apply(value, target_attribute, operation)

    	# If the object is a list
    	elif isinstance(obj, list):
    		for item in obj:
    			# Recurse into list items if they are dictionaries or lists
    			if isinstance(item, (dict, list)):
    				self.walk_and_apply(item, target_attribute, operation)

    def find_and_delete_unique(self, obj, parent=None, key_in_parent=None):
    	"""
    	Recursively searches for the 'unique' attribute in a JSON-like object, returns the value 
    	of the 'value' attribute within the same dictionary, and deletes the dictionary.

    	Args:
    	obj (dict or list): The JSON-like object to search through.
    	parent: The parent object of the current object.
    	key_in_parent: The key of the current object in the parent object.

    	Returns:
    	The value of the 'value' attribute within the dictionary that contains the 'unique' attribute, 
    	or None if not found.
    	"""

    	ret = None

    	for key in obj:
    		if 'unique' in obj[key]:
    			if obj[key]['unique'] == True:
    				return obj[key]['value']

    		if isinstance(obj[key], list):
    			for element in obj[key]:
    				ret = self.find_and_delete_unique(element) 
    				if not ret == None:
    					return ret

    		elif isinstance(obj[key], dict) and 'value' not in obj[key]:
    			ret = self.find_and_delete_unique(element) 
    			if not ret == None:
    				return ret
    				
    	return ret


    def preprocess_obj(self, obj):
    	# hash
    	self.walk_and_apply(obj, 'hash', self.hash_value)
    	self.walk_and_apply(obj, 'double_hash', self.dubble_hash)


    	unique = self.find_and_delete_unique(obj)
    	obj = self.value_is_value(obj)

    	return obj, unique


    def resolve_element(self, element):
        actual_value = element.get('value')

        ret_val = None

        if element.get('address', False):
            if not isinstance(actual_value, (bool)) and not actual_value == None:
                if isinstance(actual_value, (int, dict)) or isinstance(actual_value, float):
                    actual_value = str(actual_value)
                
                if isinstance(actual_value, list):
                    ret_val = []
                    for val in actual_value:
                        val = str(val)
                        addr, pub = WalletManager.create_batch_address(val)
                        ret_val.append(addr)

                    ret_val = str(ret_val)
                else:
                    print("actual value:")
                    print(actual_value)		
                    addr, pub = WalletManager.create_batch_address(actual_value)
                    ret_val = addr

        if element.get('reverse_address', False):
            if not isinstance(actual_value, (bool)) and not actual_value == None:
                if isinstance(actual_value, (int, dict)) or isinstance(actual_value, float):
                    actual_value = str(actual_value)
                
                if isinstance(actual_value, list):
                    ret_val = []
                    for val in actual_value:
                        val = str(val)
                        addr, pub = WalletManager.create_batch_address(val)
                        ret_val.append(addr)
                        
                    ret_val = str(ret_val)
                else:
                    print("actual value:")
                    print(actual_value)     
                    addr, pub = WalletManager.create_batch_address(actual_value)
                    ret_val = addr

        elif not element.get('clear_text', False):
            if not isinstance(actual_value, (bool)) and not actual_value == None:
                if isinstance(actual_value, (int, dict, list)) or isinstance(actual_value, float):
                    actual_value = str(actual_value)
            ret_val = self.dubble_hash(actual_value)
        else:
            ret_val = actual_value

        return ret_val

    def preprocess_clear_text(self, obj, parent=None):
    	"""
    	Recursively walks through a JSON-like object and hashes all values that are behind the 'value' key,
    	or any attribute that has a plain value that is not a bool. Does not hash if the parent object has 
    	a 'clear_text' attribute set to true.

    	Args:
    	obj (dict or list): The JSON-like object to walk through.

    	Returns:
    	None: The function modifies the object in place.
    	"""

    	# If the object is a dictionary

    	ret_obj = {}
    	if isinstance(obj, dict):
    		for key, value in list(obj.items()):
    			if not key == "_id":
    				if isinstance(value, list):
    					for x in range( 0 , len(value)):
    						ret = self.resolve_element(value[x])
    						obj[key][x] = ret
    				
    				elif isinstance(value, dict) and 'value' not in value:
    					ret = self.preprocess_clear_text(value)
    					ret_obj[key] = ret
    				else:
    					ret_obj[key] = self.resolve_element(obj[key])

    	return ret_obj


    def preprocess_save(self, obj):
    	print("IN comming obj: ")
    	print(obj)

    	unique = self.find_and_delete_unique(obj)

    	print("after delete")
    	print(unique)


    	obj = self.preprocess_clear_text(obj)

    	print("text procesing:")
    	print(obj)


    	obj = self.value_is_value(obj)

    	return obj, unique


    def parse_obj(self, obj):

    	flat = self.is_flat_json(obj)

    	print(flat)

    	tx_obj = {}

    	if flat:
    		tx_obj = self.parse_flat(obj)

    	else:
    		tx_obj = self.parse_non_flat(obj)


    	return tx_obj


    def parse_non_flat(self, obj):
    	# Convert the JSON object to a string
    	json_str = json.dumps(obj)

    	# Convert the string to hexadecimal representation
    	hex_str = binascii.hexlify(json_str.encode()).decode()

    	if len(hex_str) % 2 == 1:
    		hex_str = "0" + hex_str

    	print(hex_str)
    	return hex_str

    def parse_flat(self, obj):
    	tx_obj = {}

    	for key in obj:
    		tx_obj[key] = self.get_sat_value(obj[key])

    	return tx_obj

    def is_flat_json(self, json_obj):
    	if not isinstance(json_obj, dict):
    		return False  # Not a dictionary (JSON object)

    	for key, value in json_obj.items():
    		if isinstance(value, (dict)):
    			return False  # Nested object or array found

    	return True

    def is_float_string(self, var_input):
    	try:
    		float(var_input)
    		return True
    	except ValueError:
    		return False


    def categorize_variable(self, var_input):
    	# Check if it's an integer
    	if isinstance(var_input, int) or isinstance(var_input, float):
    		return 0

    	# Check if it's a string representing an integer
    	if isinstance(var_input, str) and (var_input.isdigit() or self.is_float_string(var_input)):
    		return 0

    	# Check if it's a date in yyyy-mm-dd format
    	date_regex = r'^\d{4}-\d{2}-\d{2}$'
    	if isinstance(var_input, str) and re.match(date_regex, var_input):
    		try:
    			datetime.strptime(var_input, '%Y-%m-%d')
    			return 1
    		except ValueError:
    			pass

    	# Otherwise, it's a string
    	return 2

    def convert_ascii_to_hex(self, string):

        if not isinstance(string, str):
            string = str(string)

        hex_str = binascii.hexlify(string.encode()).decode()

        if len(hex_str) % 2 == 1:
            hex_str = "0" + hex_str

        return hex_str

    def convert_ascii_string_to_bytes(self, string):
    	byte_value = string.encode('utf-8')
    	return list(byte_value)

    def int_array_to_satable(self, arr_int):
    	build_str = ""
    	max_len_val = 3

    	for val in arr_int:
    		str_val = str(val)
    		while len(str_val) < max_len_val:
    			str_val = "0" + str_val
    		build_str += str_val

    	return build_str

    def satable_string_to_sats(self, str_var, max_sats=100000000):
    	decrese = 0
    	n_tx = 10

    	while decrese < len(str(n_tx)):
    		decrese += 1
    		max_sats_len = len(str(max_sats)) - decrese
    		n_tx = -(len(str_var) // -max_sats_len)  # Ceiling division

    	ret = []
    	for x in range(n_tx):
    		str_x = str(x)
    		while len(str_x) < decrese:
    			str_x = "0" + str_x

    		new_str = str_var[:max_sats_len] + str_x
    		str_var = str_var[max_sats_len:]

    		while len(str_var) < len(str(max_sats)):
    			str_var = "0" + str_var

    		if (int(new_str) > 9999 ):
    			new_str = "0." + new_str
    		else:
    			new_str = "1." + new_str
    			print("new str: " + new_str)
    		ret.append(float(new_str))

    	return ret

    def convert_string_to_sats(self, string):
    	ret = self.convert_ascii_string_to_bytes(string)
    	ret = self.int_array_to_satable(ret)
    	ret = self.satable_string_to_sats(ret)
    	return ret

    def find_key(self, dictionary, string):
    	ret = self.find_key_with_prefix(dictionary, string)
    	if not ret == None:
    		return ret

    	ret = self.find_key_with_attribute(dictionary, string)
    	if not ret == None:
    		return ret

    	return False

    def find_key_with_prefix(self, dictionary, prefix):
    	prefix = prefix + "-"

    	keys = []

    	for key in dictionary:
    		if key.startswith(prefix):
    			keys.append(key)

    	if len(keys) == 1:
    		return keys[0]

    	if not len(keys) == 0:
    		return keys

    	return None

    def find_key_with_attribute(self, dictionary, attribute):

    	keys = []

    	for key in dictionary:
    		if isinstance(dictionary[key], dict):
    			if attribute in dictionary[key]:
    				if dictionary[key][attribute] == True:
    					keys.append(key)

    	if len(keys) == 1:
    		return keys[0]

    	if not len(keys) == 0:
    		return keys

    	return None

    def get_sat_value(self, value):
    	if value is None:
    		return [0]

    	cat = self.categorize_variable(value)

    	if cat == 0:  # Integer
    		if (isinstance(value, str)):
    			value = float(value)

    		if value < 10000:
    			value *= 1000
    		value /= 100000000
    		return [value]

    	elif cat == 1:  # Date
    		value = re.sub('-', '', str(value))  # Replace dashes with empty string
    		value = float(value)  # Convert to float
    		value /= 100000000
    		return [value]

    	# String part commented out as requested
    	elif cat == 2:
    	    value = self.convert_ascii_to_hex(value)
    	    pass

    	return value
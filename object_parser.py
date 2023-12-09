import re
from datetime import datetime

class ObjectParser:
	def parse_obj(self, obj):

		tx_obj = {}

		for key in obj:
			tx_obj[key] = self.get_sat_value(obj[key])

		key_found = self.find_key_with_prefix(obj, 'unique-')

		if key_found == None:
			return "no unique value provided"

		return tx_obj, key_found

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

	def find_key_with_prefix(self, dictionary, prefix):
		for key in dictionary:
			if key.startswith(prefix):
				return dictionary[key]
		return None

	def get_sat_value(self, value):
		if value is None:
			return [0]

		cat = self.categorize_variable(value)

		if cat == 0:  # Integer
			if (isinstance(value, str)):
				value = float(value)
			length = len(str(value))
			if length < 4:
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
		    value = self.convert_string_to_sats(value)
		    pass

		return value
class AddressBook:
    def __init__(self, wallet):
        self.wallet = wallet
        self.addresses = {}

    def check_balance(self):
        balance = self.wallet.get_balance()
        if balance == 0:
            return None
        else:
            return f"Balance is enough: {balance}"

    def create_oracle(self, name, description, data_type):
        return self.wallet.oracle_create(name, description, data_type)

    def send_oracle_creation_tx(self, hex_value):
        return self.wallet.sendrawtxwrapper(hex_value)

    def fund_oracle(self, oracle_txid):
        return self.wallet.oracle_fund(oracle_txid)

    def register_as_publisher(self, oracle_txid, data_fee):
        return self.wallet.oracle_register(oracle_txid, data_fee)

    def send_register_tx(self, register_hex):
        return self.wallet.sendrawtxwrapper(register_hex)

    def subscribe_to_oracle(self, oracle_txid, publisher_id, fee):
        return self.wallet.oracle_subscribe(oracle_txid, publisher_id, fee)

    def publish_data_to_oracle(self, oracle_txid, data_string):
        # Convert the string to UTF-8 bytes and then to a hex string
        hex_data = data_string.encode('utf-8').hex()

        # Get the length of the original data string
        data_length = len(data_string)

        # Convert the length to a hex string
        length_hex = format(data_length, 'x')

        # Concatenate the length in hex and the data hex string
        final_hex_data = length_hex + hex_data

        # Send the data to the oracle
        return self.wallet.oracle_data(oracle_txid, final_hex_data)

    def get_oracle_info(self, oracle_txid):
        return self.wallet.oracle_info(oracle_txid)

    def create_string_oracle(self, name, description):
        # Call the oracle_create method from the wallet object
        res = self.wallet.oracle_create(name, description, "s")

        # Check if the creation was successful
        if not res.get('result') == 'success':
            error_message = res.get('error', 'Unknown error')
            print(f"Oracle creation failed: {error_message}")
            raise Exception(f"Oracle creation failed: {error_message}")
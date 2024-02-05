class AddressBook:
    def __init__(self, wallet):
        self.wallet = wallet
        self.addresses = {}

    def add_address(self, name, address):
        """ Adds an address with a corresponding name to the address book. """
        self.addresses[name] = address

    def get_address(self, name):
        """ Retrieves an address by its name from the address book. """
        return self.addresses.get(name, None)

    def remove_address(self, name):
        """ Removes an address from the address book. """
        if name in self.addresses:
            del self.addresses[name]

    def list_addresses(self):
        """ Lists all addresses in the address book. """
        return self.addresses
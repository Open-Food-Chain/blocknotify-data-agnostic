import re
import os
import http
import platform
import random
import string
import datetime
from slickrpc import Proxy

from komodo_py.node_rpc import NodeRpc
from komodo_py.explorer import QueryInterface
from komodo_py.explorer import Explorer
from komodo_py.wallet import WalletInterface
from komodo_py.oracles import Oracles

from oracles_manager import OraclesManager
from wallet_manager import WalManInterface

import os
from dotenv import load_dotenv

load_dotenv()

user_name = os.getenv('BATCH_SMARTCHAIN_NODE_USERNAME')
password = os.getenv('BATCH_SMARTCHAIN_NODE_PASSWORD')
rpc_port = int(os.getenv('BATCH_SMARTCHAIN_NODE_RPC_PORT'))
private_key = os.getenv('THIS_NODE_WIF')
ip_address = os.getenv('BATCH_SMARTCHAIN_NODE_IPV4_ADDR')


node_rpc = NodeRpc(user_name, password, rpc_port, private_key, ip_address)

#query = QueryInterface(node_rpc)

#oracle_man = Oracles(query)

#ex = Explorer("https://ofcmvp.explorer.batch.events/")

explorer_url = os.getenv('EXPLORER_URL')
seed = os.getenv('SEED')
import_api_host = os.getenv('IMPORT_API_HOST')
import_api_port = int(os.getenv('IMPORT_API_PORT'))
chain_api_host = os.getenv('CHAIN_API_HOST')
chain_api_port = int(os.getenv('CHAIN_API_PORT'))
collections = os.getenv('COLLECTIONS').split(',')  # Assuming 'collections' is a comma-separated list
print(collections)
min_utxos = int(os.getenv('MIN_UTXOS'))
min_balance = int(os.getenv('MIN_BALANCE'))

#ret = node_rpc.getinfo()
#print(ret)

#ret = node_rpc.get_balance("test")
#print(ret)

#ret = node_rpc.get_rawtransaction("fb5e0c9fbcf43ade68e7ab9b5bd5774264f80568743c3e8f1b1ef377b604d288")
#print(ret)

def random_digits(length):
    """Generate a random string of digits with fixed length."""
    return ''.join(random.choices(string.digits, k=length))

def random_string(length):
    """Generate a random string of letters and digits with fixed length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def random_date(start, end):
    """Generate a random date between `start` and `end`."""
    delta = end - start
    return start + datetime.timedelta(days=random.randint(0, delta.days))

def generate_test_batches(num_batches):
    batches = []
    for _ in range(num_batches):
        batch = {
            "anfp": random_digits(8),  # Assuming this should be digits only
            "dfp": random_string(16),
            "bnfp": random_digits(6),
            "pds": str(random_date(datetime.date(2020, 1, 1), datetime.date(2020, 12, 31))),
            "pde": str(random_date(datetime.date(2020, 1, 1), datetime.date(2020, 12, 31))),
            "jds": random.randint(1, 10),
            "jde": random.randint(1, 10),
            "bbd": str(random_date(datetime.date(2020, 1, 1), datetime.date(2020, 12, 31))),
            "pc": random_string(2),
            "pl": { "value":random_string(7), "hash":True},
            "rmn": random_digits(8),
            "pon": random_digits(6),
            "pop": random_digits(3),
            "mass": round(random.uniform(0.5, 2.0), 1),
            "integrity_details": None,
            "percentage": None
        }
        batches.append(batch)
    
    return batches

to_remove = []

test_batch = generate_test_batches(1)[0]

wal_in = WalletInterface(node_rpc, "pact_image_wheat_cheese_model_daring_day_only_setup_cram_leave_good_limb_dawn_diagram_kind_orchard_pelican_chronic_repair_rack_oxygen_intact_vanish", True)

or_man = OraclesManager(wal_in, "chris8")

all_wall_man = WalManInterface(wal_in, explorer_url, test_batch, to_remove, or_man, "batch")

#ret = or_man.subscribe_to_org_oracle()

#ret = or_man.search_this_org_oracles("Address_Bookchris8")
#print(ret)


#ret = wal_in.get_wif()
#print(ret)

#ret = wal_in.get_oracle_list()
#print(ret)

#ret = wal_in.create_string_oracle("test2", "this is a filler oracle test test test", "1000000")

#print("txid: " + str(ret))

#ret = wal_in.get_oracle_info("8965b3fb8e3db3b128028ae15ef22ffda960506ba13758a7ee622e4016205433")
#print(ret)

#ret = wal_in.subscribe_to_oracle("8965b3fb8e3db3b128028ae15ef22ffda960506ba13758a7ee622e4016205433", "1")
#print(ret)

#ret = node_rpc.get_rawtransaction(ret)
#print(ret)

#ret = ex.broadcast(ret)
#print(ret)

#ret = wal_in.publish_data_string_to_oracle("8965b3fb8e3db3b128028ae15ef22ffda960506ba13758a7ee622e4016205433", "test")
#print(ret)

#wal_in = WalletInterface(node_rpc, "pact_image_wheat_cheese_model_daring_day_only_setup_cram_leave_good_limb_dawn_diagram_kind_orchard_pelican_chronic_repair_rack_oxygen_intact_vanish")

#addy_book = AddressBook(wal_in)


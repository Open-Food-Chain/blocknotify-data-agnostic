from komodo_py.transaction import TxInterface
from komodo_py.explorer import Explorer
from komodo_py.wallet import WalletInterface
from ecpy.curves     import Curve,Point
import hashlib
import ecdsa
import time

from wallet_manager import WalManInterface
from object_parser import ObjectParser
from import_manager import ImportManInterface
from chain_api_manager import ChainApiInterface

import os
from dotenv import load_dotenv

load_dotenv()

# Reading environment variables
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


def get_wals(import_manager, wal_in):
    first_items = import_manager.get_first_items()
    to_remove = ["integrity_details", "id", "created_at", "raw_json", "bnfp", "_id"]
    all_wall_man = {}

    for collection_name, test_batch in first_items.items():
        if isinstance(test_batch, dict):  # Ensure that test_batch is a dictionary
            all_wall_man[collection_name] = WalManInterface(wal_in, explorer_url, test_batch, to_remove)

    return all_wall_man


def init_blocknotify(explorer_url, seed, import_api_host, import_api_port, chain_api_host, chain_api_port, collection_names):
    explorer = Explorer(explorer_url)
    wal_in = WalletInterface(explorer, seed)
    import_man_interface = ImportManInterface(import_api_host, import_api_port, collection_names)  
    chain_api_manager =   ChainApiInterface(chain_api_host, chain_api_port)
    all_wall_man = get_wals(import_man_interface, wal_in)

    res = chain_api_manager.check_org(wal_in.get_address())

    
    for name in all_wall_man:
        all_wall_man[name].start_utxo_manager(min_utxos, min_balance)

    return wal_in, import_man_interface, all_wall_man, chain_api_manager


def main_loop_blocknotify(wal_in, import_man_interface, all_wall_man, chain_api_manager):
    items_without_integrity = import_man_interface.get_imports_without_integrity()
    obj_parser = ObjectParser()

    if len(all_wall_man) == 0:
        return "no items try later"

    for collection_name, items in items_without_integrity.items():
        print(collection_name)
        print(items)
        wal_man = all_wall_man[collection_name]
        for item in items:
            print(item)
            
            tx_obj, unique_attribute = obj_parser.preprocess_save(item)

            if unique_attribute:
                tx_obj = obj_parser.parse_obj(tx_obj)
                
                print(tx_obj)
                print(unique_attribute)
                ret = wal_man.send_batch_transaction(tx_obj, unique_attribute)
                print("int details: ")
                print(ret)
                if not (isinstance(ret, str )):
                    update_integrity = import_man_interface.add_integrity_details(collection_name, item['_id'], ret)
                    res = chain_api_manager.add_batch(ret["unique-addr"], ret["unique-pub"], wal_in.get_address(), item)
                    print(update_integrity)
                #    print("chain manager: " + str(res))
                else:
                    time.sleep(30)

            else:
                print("missing unique attribute ")
        
    for wal in all_wall_man:
        all_wall_man[wal].stop_utxo_manager()

    return "sucses"


explorer = Explorer(explorer_url)
wal_in = WalletInterface(explorer, seed)

wal_in, import_man_interface, all_wall_man, chain_api_manager = init_blocknotify(explorer_url, seed, import_api_host, import_api_port,  chain_api_host, chain_api_port, collections)

ret = main_loop_blocknotify(wal_in, import_man_interface, all_wall_man, chain_api_manager)

print(ret)

print("exit with")
print("#########")
print(ret)
print("tegar is cool")
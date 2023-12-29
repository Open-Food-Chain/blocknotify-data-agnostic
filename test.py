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


wal_in = WalletInterface(explorer_url, seed)
#print(wal_in.send_tx_force( ["RA6kFZkA3oVrQjPGbuoxmZDaHvMp9sMhgg", "RFuBZNJCWiwW7a7TradLPLvwymooPRzsGR"], [1, 1] ))

test_batch = {
    "id": "b6c23100-bb41-4477-b0a5-f72e8504c9fb",
    "anfp": "11000011",
    "dfp": "Description here",
    "bnfp": "637893",
    "pds": "2020-03-01",
    "pde": "2020-03-05",
    "jds": 2,
    "jde": 7,
    "bbd": "2020-05-05",
    "pc": "DE",
    "pl": "Herrath",
    "rmn": "11200100",
    "pon": "123072",
    "pop": "164",
    "mass": 1.0,
    "raw_json": "eyBcImFuZnBcIjogXCIxMTAwMDAxMVwiLFwiZGZwXCI6IFwiRGVzY3JpcHRpb24gaGVyZVwiLFwiYm5mcFwiOiBcIjYzNzg5M1wiLFwicGRzXCI6IFwiMjAyMC0wMy0xXCIsXCJwZGVcIjogXCIyMDIwLTAzLTVcIixcImpkc1wiOiAyLFwiamRlXCI6IDcsXCJiYmRcIjogXCIyMDIwLTA1LTVcIixcInBjXCI6IFwiREVcIixcInBsXCI6IFwiSGVycmF0aFwiLFwicm1uXCI6IFwiMTEyMDAxMDA1MjBcIixcInBvblwiOiBcIjEyMzA3MlwiLFwicG9wXCI6IFwiMTY0XCIK",
    "integrity_details": None,
    "created_at": "2023-09-25T08:21:45.070925Z",
    "percentage": None
}

def get_wals(import_manager, wal_in):
    first_items = import_manager.get_first_items()
    to_remove = ["integrity_details", "id", "created_at", "raw_json", "bnfp", "_id"]
    all_wall_man = {}

    for collection_name, test_batch in first_items.items():
        if isinstance(test_batch, dict):  # Ensure that test_batch is a dictionary
            all_wall_man[collection_name] = WalManInterface(wal_in, test_batch, to_remove)

    return all_wall_man


def init_blocknotify(explorer_url, seed, import_api_host, import_api_port, chain_api_host, chain_api_port, collection_names):
    wal_in = WalletInterface(explorer_url, seed)
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

    for collection_name, items in items_without_integrity.items():
        wal_man = all_wall_man[collection_name]
        for item in items:
            print(item)
            tx_obj, unique_attribute = obj_parser.parse_obj(item)
            print(tx_obj)
            print(unique_attribute)
            ret = wal_man.send_batch_transaction(tx_obj, unique_attribute)
            print(ret)
            if not (isinstance(ret, str )):
                update_integrity = import_man_interface.add_integrity_details(collection_name, item['_id'], ret)
                chain_api_manager.add_batch(ret["unique-addr"], ret["unique-pub"], wal_in.get_address(), item)
                print(update_integrity)
            else:
                time.sleep(30)

    
    #for wal in all_wall_man:
    #    all_wall_man[wal].stop_utxo_manager()

    return "sucses"




wal_in, import_man_interface, all_wall_man, chain_api_manager = init_blocknotify(explorer_url, seed, import_api_host, import_api_port,  chain_api_host, chain_api_port, collections)

#ret = wal_in.send_tx_opreturn(wal_in.get_address(), "7b22")
#print(ret)


#ret = all_wall_man['batch'].start_utxo_manager(min_utxos, min_balance)
#print(ret)

#time.sleep(10)

#ret = all_wall_man['batch'].stop_utxo_manager()
#print(ret)

#print(wal_in.get_address())

#ret = all_wall_man["batch"].fund_offline_wallets()
#print(ret)

main_loop_blocknotify(wal_in, import_man_interface, all_wall_man, chain_api_manager)


"""import_man_interface = ImportManInterface("127.0.0.1", 5000, ["batch"])
all_imports_without_integrity = import_man_interface.get_imports_without_integrity()
print(all_imports_without_integrity)"""

#to_remove = ["integrity_details", "id", "created_at", "raw_json", "bnfp" ]

#walManIn = WalManInterface(wal_in, test_batch, to_remove)

#obj_parser = ObjectParser()

#tx_obj = obj_parser.parse_obj(test_batch)
#print(tx_obj)

#ret = walManIn.send_batch_transaction(tx_obj, test_batch["bnfp"])
#print(ret)

#print(walManIn.fund_offline_wallets())



#print(chain_api_manager.add_batch("RMXqGFHvYf5eRPkhSnLN19bx91qrS8ys9N", "020293989838484848488484849485948594859485948594850948594898498898", wal_in.get_address(), test_batch))
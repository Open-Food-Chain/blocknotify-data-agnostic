from komodo_py.transaction import TxInterface
from komodo_py.explorer import Explorer
from komodo_py.wallet import WalletInterface
from komodo_py.node_rpc import NodeRpc

from ecpy.curves import Curve, Point
import hashlib
import ecdsa
import time

from wallet_manager import WalManInterface
from object_parser import ObjectParser
from import_manager import ImportManInterface
from chain_api_manager import ChainApiInterface
from oracles_manager import OraclesManager
from scraper import Scraper

import os
from dotenv import load_dotenv

load_dotenv()


class BlockNotify:
    def __init__(self, explorer_url, seed, import_api_host, import_api_port, chain_api_host, chain_api_port, collection_names):
        self.explorer_url = explorer_url
        self.seed = seed
        self.import_api_host = import_api_host
        self.import_api_port = import_api_port
        self.chain_api_host = chain_api_host
        self.chain_api_port = chain_api_port
        self.collection_names = collection_names
        self.init_blocknotify()

    def init_blocknotify(self):
        self.node_rpc = NodeRpc(os.getenv('BATCH_SMARTCHAIN_NODE_USERNAME'), os.getenv('BATCH_SMARTCHAIN_NODE_PASSWORD'), int(os.getenv('BATCH_SMARTCHAIN_NODE_RPC_PORT')), os.getenv('THIS_NODE_WIF'), os.getenv('BATCH_SMARTCHAIN_NODE_IPV4_ADDR'))
        self.wal_in = WalletInterface(self.node_rpc, self.seed, True)
        self.import_man_interface = ImportManInterface(self.import_api_host, self.import_api_port, self.collection_names)
        self.chain_api_manager = ChainApiInterface(self.chain_api_host, self.chain_api_port)
        self.all_wall_man = self.get_wals(self.import_man_interface, self.wal_in, self.node_rpc)
        self.check_env(self.wal_in)

    def get_wals(self, import_manager, wal_in, node):
        first_items = import_manager.get_first_items()
        to_remove = ["integrity_details", "id", "created_at", "raw_json", "bnfp", "_id"]
        all_wall_man = {}
        for collection_name, test_batch in first_items.items():
            if isinstance(test_batch, dict):
                or_man = OraclesManager(wal_in, os.getenv('ORG_NAME'))
                all_wall_man[collection_name] = WalManInterface(wal_in, self.explorer_url, test_batch, to_remove, or_man, collection_name)
                scraper = Scraper(node=node, explorer_url=self.explorer_url, oracle_manager=or_man, collections=[collection_name])
                block = scraper.scan_blocks()
        return all_wall_man

    def check_env(self, wal_in):
        err = False
        addy = wal_in.get_address()
        pub = wal_in.get_public_key()
        wif = wal_in.get_wif()
        if addy != os.getenv('THIS_NODE_RADDRESS') or pub != os.getenv('THIS_NODE_PUBKEY') or wif != os.getenv('THIS_NODE_WIF'):
            print("Environment validation failed:")
            print(f"Address should be: {addy}")
            print(f"Pubkey should be: {pub}")
            print(f"Privkey should be: {wif}")
            err = True
        if err:
            exit()


    def send_batch(self, item, collection_name):
        obj_parser = ObjectParser()
        tx_obj, unique_attribute = obj_parser.preprocess_save(item)
        tx_obj, unique_attribute = obj_parser.parse_obj(tx_obj)
        wal_man = self.all_wall_man.get(collection_name, None)
        if wal_man:
            ret = wal_man.send_batch_transaction(tx_obj, unique_attribute, collection_name)
            return ret
        else:
            return "Wallet manager not found for the specified collection."

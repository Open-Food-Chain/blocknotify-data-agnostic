import re
import os
import http
import platform
from slickrpc import Proxy

from komodo_py.node_rpc import NodeRpc
from komodo_py.explorer import QueryInterface
from komodo_py.explorer import Explorer
from komodo_py.wallet import WalletInterface
from komodo_py.oracles import Oracles

from address_book import AddressBook

import os
from dotenv import load_dotenv

load_dotenv()

user_name = os.getenv('BATCH_SMARTCHAIN_NODE_USERNAME')
password = os.getenv('BATCH_SMARTCHAIN_NODE_PASSWORD')
rpc_port = int(os.getenv('BATCH_SMARTCHAIN_NODE_RPC_PORT'))
private_key = os.getenv('THIS_NODE_WIF')
ip_address = os.getenv('BATCH_SMARTCHAIN_NODE_IPV4_ADDR')


node_rpc = NodeRpc(user_name, password, rpc_port, private_key, "127.0.0.1")

#query = QueryInterface(node_rpc)

#oracle_man = Oracles(query)

ex = Explorer("https://ofcmvp.explorer.batch.events/")



ret = node_rpc.getinfo()
print(ret)

#ret = node_rpc.get_rawtransaction("fb5e0c9fbcf43ade68e7ab9b5bd5774264f80568743c3e8f1b1ef377b604d288")
#print(ret)

wal_in = WalletInterface(node_rpc, "pact_image_wheat_cheese_model_daring_day_only_setup_cram_leave_good_limb_dawn_diagram_kind_orchard_pelican_chronic_repair_rack_oxygen_intact_vanish", True)

#ret = wal_in.create_string_oracle("filler", "this is a filler oracle", "0.9")

#print("txid: " + str(ret))

#ret = wal_in.get_oracle_info("695a79f039dbc241465f844c111cbfab0273942b67ca05f4c7b5b4b86b1b2e4b")
#print(ret)

ret = wal_in.subscribe_to_oracle("695a79f039dbc241465f844c111cbfab0273942b67ca05f4c7b5b4b86b1b2e4b", "1")
print(ret)

ret = node_rpc.get_rawtransaction(ret)
print(ret)

ret = ex.broadcast(ret)
print(ret)

#ret = wal_in.publish_data_string_to_oracle("695a79f039dbc241465f844c111cbfab0273942b67ca05f4c7b5b4b86b1b2e4b", "test")
#print(ret)

#wal_in = WalletInterface(node_rpc, "pact_image_wheat_cheese_model_daring_day_only_setup_cram_leave_good_limb_dawn_diagram_kind_orchard_pelican_chronic_repair_rack_oxygen_intact_vanish")

#addy_book = AddressBook(wal_in)


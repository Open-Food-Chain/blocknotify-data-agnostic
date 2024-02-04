import re
import os
import http
import platform
from slickrpc import Proxy

from komodo_py.node_rpc import NodeRpc

import os
from dotenv import load_dotenv

load_dotenv()

user_name = os.getenv('BATCH_SMARTCHAIN_NODE_USERNAME')
password = os.getenv('BATCH_SMARTCHAIN_NODE_PASSWORD')
rpc_port = int(os.getenv('BATCH_SMARTCHAIN_NODE_RPC_PORT'))
private_key = os.getenv('THIS_NODE_WIF')
ip_address = os.getenv('BATCH_SMARTCHAIN_NODE_IPV4_ADDR')


node_rpc = NodeRpc(user_name, password, rpc_port, private_key, "127.0.0.1")

# Make the getinfo call
try:
    info = node_rpc.getinfo()
    print("Node Info:", info)
except Exception as e:
    print(f"Error: {e}")

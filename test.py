from komodo_py.transaction import TxInterface
from komodo_py.explorer import Explorer
from komodo_py.wallet import WalletInterface
from ecpy.curves     import Curve,Point
import hashlib
import ecdsa


wal_in = WalletInterface("https://ofcmvp.explorer.batch.events/", "pact_image_wheat_cheese_model_daring_day_only_setup_cram_leave_good_limb_dawn_diagram_kind_orchard_pelican_chronic_repair_rack_oxygen_intact_vanish")
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
    "rmn": "11200100520",
    "pon": "123072",
    "pop": "164",
    "mass": 1.0,
    "raw_json": "eyBcImFuZnBcIjogXCIxMTAwMDAxMVwiLFwiZGZwXCI6IFwiRGVzY3JpcHRpb24gaGVyZVwiLFwiYm5mcFwiOiBcIjYzNzg5M1wiLFwicGRzXCI6IFwiMjAyMC0wMy0xXCIsXCJwZGVcIjogXCIyMDIwLTAzLTVcIixcImpkc1wiOiAyLFwiamRlXCI6IDcsXCJiYmRcIjogXCIyMDIwLTA1LTVcIixcInBjXCI6IFwiREVcIixcInBsXCI6IFwiSGVycmF0aFwiLFwicm1uXCI6IFwiMTEyMDAxMDA1MjBcIixcInBvblwiOiBcIjEyMzA3MlwiLFwicG9wXCI6IFwiMTY0XCIK",
    "integrity_details": None,
    "created_at": "2023-09-25T08:21:45.070925Z",
    "percentage": None
}


def get_wallet_address(sig_key, string):
    string = string.encode('utf-8')
    sig = sig_key.sign_digest_deterministic(string, hashfunc=hashlib.sha256, sigencode = ecdsa.util.sigencode_der_canonize)
    return sig

def encode_base58(buffer):
    ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

    # Convert the buffer to a list of integers for easier processing
    digits = [0]
    for byte in buffer:
        carry = byte
        for j in range(len(digits)):
            carry += digits[j] << 8
            digits[j] = carry % 58
            carry //= 58
        while carry > 0:
            digits.append(carry % 58)
            carry //= 58

    # Remove leading zeros
    zero_count = 0
    for byte in buffer:
        if byte == 0:
            zero_count += 1
        else:
            break

    # Convert digits to Base58 string
    return ALPHABET[digits.pop()] + ALPHABET[0] * zero_count + ''.join(ALPHABET[d] for d in reversed(digits))

def get_wallets(wal_in, dict_obj):
    name_and_wal = {}

    for key in dict_obj:
        sign_key = wal_in.get_sign_key()
        new_seed = encode_base58(get_wallet_address(sign_key, key))
        new_wallet = WalletInterface("https://ofcmvp.explorer.batch.events/", new_seed)
        name_and_wal[key] = new_wallet

    return name_and_wal

def remove_keys_from_json_object(json_object, keys_to_remove):
    new_obj = json_object.copy()  # Create a shallow copy of the original dictionary
    for key in keys_to_remove:
        new_obj.pop(key, None)  # Remove the key if it exists
    return new_obj


def create_batch_address( wal_in, batch_value ):
    sign_key = wal_in.get_sign_key()
    new_seed = encode_base58(get_wallet_address(sign_key, batch_value))
    new_wallet = WalletInterface("https://ofcmvp.explorer.batch.events/", new_seed)
    return new_wallet.get_address()

def fund_offline_wallets( wal_in, walls):
    

sign_key = wal_in.get_sign_key()

#new_seed = encode_base58(get_wallet_address(sign_key, "test"))

#new_wallet = WalletInterface("https://ofcmvp.explorer.batch.events/", new_seed)

batch_addr = create_batch_address(wal_in, test_batch["bnfp"])

to_remove = ["integrity_details", "id", "created_at", "raw_json", "bnfp" ]

clean_test_batch = remove_keys_from_json_object(test_batch, to_remove)



wals = get_wallets(wal_in, clean_test_batch)

#for key in wals:
#    print("key: " + key + ", addr: " + wals[key].get_address())

print(wal_in.get_utxos())


"""tx_in = TxInterface(ex, wal)

for n in range(0, 1000):
	rawtx = tx_in.send_tx_force( ["RA6kFZkA3oVrQjPGbuoxmZDaHvMp9sMhgg", "RFuBZNJCWiwW7a7TradLPLvwymooPRzsGR"], [1, 1] )

print(rawtx)

#res = ex.broadcast_via_explorer( rawtx )
#print(res)
"""

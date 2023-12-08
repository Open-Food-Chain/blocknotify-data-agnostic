from komodo_py.transaction import TxInterface
from komodo_py.explorer import Explorer
from komodo_py.wallet import WalletInterface
from ecpy.curves     import Curve,Point
import hashlib
import ecdsa

from wallet_manager import WalManInterface
from object_parser import ObjectParser

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
    "rmn": "11200100",
    "pon": "123072",
    "pop": "164",
    "mass": 1.0,
    "raw_json": "eyBcImFuZnBcIjogXCIxMTAwMDAxMVwiLFwiZGZwXCI6IFwiRGVzY3JpcHRpb24gaGVyZVwiLFwiYm5mcFwiOiBcIjYzNzg5M1wiLFwicGRzXCI6IFwiMjAyMC0wMy0xXCIsXCJwZGVcIjogXCIyMDIwLTAzLTVcIixcImpkc1wiOiAyLFwiamRlXCI6IDcsXCJiYmRcIjogXCIyMDIwLTA1LTVcIixcInBjXCI6IFwiREVcIixcInBsXCI6IFwiSGVycmF0aFwiLFwicm1uXCI6IFwiMTEyMDAxMDA1MjBcIixcInBvblwiOiBcIjEyMzA3MlwiLFwicG9wXCI6IFwiMTY0XCIK",
    "integrity_details": None,
    "created_at": "2023-09-25T08:21:45.070925Z",
    "percentage": None
}


to_remove = ["integrity_details", "id", "created_at", "raw_json", "bnfp" ]

walManIn = WalManInterface(wal_in, test_batch, to_remove)

obj_parser = ObjectParser()

tx_obj = obj_parser.parse_obj(test_batch)
print(tx_obj)

ret = walManIn.send_batch_transaction(tx_obj, test_batch["bnfp"])
print(ret)

#print(walManIn.fund_offline_wallets())


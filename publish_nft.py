import json
import hashlib
from algosdk import mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import AssetConfigTxn, wait_for_confirmation
from infura_wrapper import infura_wrapper
from db import DB

# Change algod_token and algod_address to connect to a different client
# algod_token = "2f3203f21e738a1de6110eba6984f9d03e5a95d7a577b34616854064cf2c0e7b"
# algod_address = "https://academy-algod.dev.aws.algodev.network/"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
algod_address = "http://localhost:4001"
algod_client = algod.AlgodClient(algod_token, algod_address)

# Sample account
test_account_address = "EXT2OCCMAY3DXWV5IVQDJO2KGRO3VORNPEIR3UXZ5LDUONJLNXHZNBJNLA"
test_account_mnemonic = "bronze predict balance differ critic state engage height stumble abandon answer loud else stuff wrist canvas join sorry belt impulse make embody guilt ability secret"
pk = mnemonic.to_public_key(test_account_mnemonic)
sk = mnemonic.to_private_key(test_account_mnemonic)


def publish_nft(unit_name, asset_name, metadata):
    print("--------------------------------------------")
    print("Creating Asset...")
    # CREATE ASSET
    # Get network params for transactions before every transaction.
    params = algod_client.suggested_params()

    cid = infura_wrapper(metadata)
    hash = hashlib.new("sha512_256")
    hash.update(b"arc0003/amj")
    hash.update(metadata.encode("utf-8"))
    json_metadata_hash = hash.digest()

    # Account 1 creates an asset called latinum and
    # sets Account 1 as the manager, reserve, freeze, and clawback address.
    # Asset Creation transaction
    assetURL = "ipfs://" + cid
    txn = AssetConfigTxn(
        sender=pk,
        sp=params,
        total=1,
        default_frozen=False,
        unit_name=unit_name,
        asset_name=asset_name,
        manager=None,
        reserve=None,
        freeze=None,
        clawback=None,
        strict_empty_address_check=False,
        url=assetURL,
        metadata_hash=json_metadata_hash,
        decimals=0)

    # Sign with secret key of creator
    stxn = txn.sign(sk)

    try:
        # Send the transaction to the network and retrieve the txid.
        txid = algod_client.send_transaction(stxn)
        print("Asset Creation Transaction ID: {}".format(txid))
    
        DB().insert_asset(('ARC-0003', test_account_address, cid, assetURL))
        DB().insert_transaction((txid, 'EXECUTING'))
        
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
        DB().update_transaction_status(txid, 'SUCCESS')
    except Exception as e:
        print(e)
        DB().update_transaction_status(txid, 'FAIL')
        
    return txid


def get_info_asset(txid):
    try:
        # Get the new asset's information from the creator account
        ptx = algod_client.pending_transaction_info(txid)
        asset_id = ptx["asset-index"]
        account_info = algod_client.account_info(pk)
        idx = 0
        for my_account_info in account_info['created-assets']:
            scrutinized_asset = account_info['created-assets'][idx]
            idx = idx + 1       
            if (scrutinized_asset['index'] == asset_id):
                print("Asset ID: {}".format(scrutinized_asset['index']))
                return json.dumps(my_account_info['params'], indent=4)
    except Exception as e:
        print(e)
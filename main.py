from flask import Flask, request
from publish_nft import publish_nft, get_info_asset
from db import DB

app = Flask(__name__)
DB().init_tables()

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.post("/publish-nft")
def publish_nfts():
    unit_name = request.form['unit_name']
    asset_name = request.form['asset_name']
    metadata = request.form['metadata']

    # Execute from here
    txid = publish_nft(unit_name, asset_name, metadata)
    asset_info = get_info_asset(txid)
    return  asset_info


@app.errorhandler(404)
def page_not_found(error):
    return "Handler not found", 404

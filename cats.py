from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import time
from beem import Steem
from beem.nodelist import NodeList
from steemengine.api import Api
from steemengine.wallet import Wallet

if __name__ == "__main__":
    nodelist = NodeList()
    nodelist.update_nodes()
    stm = Steem(node=nodelist.get_nodes())
    api = Api()
    wallet = Wallet("ufm.pay")

    # edit here
    upvote_account = "ufm.pay"
    upvote_token = "KITTENS"
    token_weight_factor = 1  # multiply token amount to get weight
    kitten_ratio = 20
    stm = Steem()
    stm.wallet.unlock(pwd="")
    wallet = Wallet(upvote_account, steem_instance=stm)
    stamps = []
    whitelist = []
    blacklist = ["market", "tokens"]
    last_steem_block = 1950  # It is a good idea to store this block, otherwise all transfers will be checked again
    while True:
        main_token = wallet.get_token("CATS")
        history = api.get_history(upvote_account, upvote_token, limit=1000, offset=0, histtype='user')
        for h in history:
            if int(h["block"]) <= last_steem_block:
                continue
            if h["to"] != upvote_account:
                continue
            last_steem_block = int(h["block"])
            if len(whitelist) > 0 and h["from"] not in whitelist:
                print("%s is not in the whitelist, skipping" % h["from"])
                continue
            if len(blacklist) > 0 and h["from"] in blacklist:
                print("blacklisted user, skipping...")
                continue
            if float(h["quantity"]) < kitten_ratio:
                print("Below min token amount skipping...")
                print(wallet.transfer(h["from"], float(h["quantity"]), "KITTENS", "Refund - Below minimum!"))
                print("refund sent")
                continue
            if float(h["quantity"]) % 20:
                print("incorrect ratio, skipping...")
                print(wallet.transfer(h["from"], float(h["quantity"]), "KITTENS", "Refund - Amount must be a multiple of the current ratio!"))
                print("refund sent...")
                continue
            if main_token is not None and float(main_token["balance"]) >= 1:
                print("balance %.2f" % float(main_token["balance"]))
                print(wallet.transfer(h["from"], float(h["quantity"]) / kitten_ratio, "CATS", "Here are your CATS!"))
        time.sleep(4)

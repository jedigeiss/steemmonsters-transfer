#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 08:35:15 2018

@author: jan
"""

from beem.blockchain import Blockchain
from beem.nodelist import NodeList
from beem import Steem
from beem.account import Account
import json
import getpass
import time
import requests
import os
from os.path import exists
from time import sleep
import sys
from beem.exceptions import AccountDoesNotExistsException
from beemapi.exceptions import ApiNotSupported



__url__ = 'https://steemmonsters.com/'


def read_config_json(config_json, verbose=True):
    if not exists(config_json):
        if verbose:
            print("Could not find config json: %s" % config_json)
        sm_config = {}
    else:
        sm_config = json.loads(open(config_json).read())
    return sm_config

# initialize the card dict holding names and ids
card_dict = {}

wss = False
https = True
normal = False
appbase = True
config_file_name = "config.json"
sm_config = read_config_json(config_file_name, verbose=False)
if "wallet_password" in sm_config:
    wallet_pass = sm_config["wallet_password"]
else:
    wallet_pass = getpass.getpass(prompt='Enter the beem wallet password.')
nodes = NodeList()
nodes.update_nodes()
nodelist = nodes.get_nodes(normal=normal, appbase=appbase, wss=wss, https=https)
stm = Steem(node=nodelist, num_retries=5, call_num_retries=3, timeout=15)
stm.wallet.unlock(wallet_pass)
#print(nodes) 


#def get_card_details():
#    response = ""
#    cnt2 = 0
#    count = 0
#    while str(response) != '<Response [200]>' and cnt2 < 15:
#        response = requests.get(__url__ + "cards/get_details")
#        if str(response) != '<Response [200]>':
#            time.sleep(1)
#        cnt2 += 1
#    for r in response.json():
#        card_dict[r["name"]] = r["id"]
#        count +=1
   
# =============================================================================
# def check_decks():
#     card1 = "medusa"
#     if card1 in card_dict:
#         print("hello")
# =============================================================================


def check_account(to):
    try:
        account = Account(to)
    except TypeError:
        #print(err)
        return -1
    except AccountDoesNotExistsException:
        return -1
    except ApiNotSupported:
        return -2
    return 0
    

def get_player_deck(player, color):
    response = ""
    cnt2 = 0
    while str(response) != '<Response [200]>' and cnt2 < 15:
        response = requests.get(__url__ + "cards/collection/" + player)
        if str(response) != '<Response [200]>':
            sleep(1)
        cnt2 += 1
    data = response.json()
    json = []
    for r in data["cards"]:
        uid = r["uid"]
        card_detail_id = r["card_detail_id"]
        market_id = r["market_id"]
        if color == "red" and market_id is None:    
            if card_detail_id > 0 and card_detail_id < 12:
                string = ("%s" % uid)
                json.append(string)
            elif card_detail_id == 70:
                string = ("%s" % uid)
                json.append(string)
        if color == "blue" and market_id is None:
            if card_detail_id > 11 and card_detail_id < 23:
                string = ("%s" % uid)
                json.append(string)
            elif card_detail_id == 71:
                string = ("%s" % uid)
                json.append(string)
        if color == "green" and market_id is None:
            if card_detail_id > 22 and card_detail_id < 34:
                string = ("%s" % uid)
                json.append(string)
            elif card_detail_id == 72:
                string = ("%s" % uid)
                json.append(string)
        if color == "white" and market_id is None:
            if card_detail_id > 33 and card_detail_id < 45:
                string = ("%s" % uid)
                json.append(string)
            elif card_detail_id == 73:
                string = ("%s" % uid)
                json.append(string)
        if color == "black" and market_id is None :
            if card_detail_id > 44 and card_detail_id < 56:
                string = ("%s" % uid)
                json.append(string)
            elif card_detail_id == 74:
                string = ("%s" % uid)
                json.append(string)
        if color == "neutral" and market_id is None:
            if card_detail_id > 59 and card_detail_id < 70:
                string = ("%s" % uid)
                json.append(string)
        if color == "gold" and market_id is None:
            if card_detail_id > 55 and card_detail_id < 60:
                string = ("%s" % uid)
                json.append(string)
            elif card_detail_id >= 76 and card_detail_id <= 78 :
                string = ("%s" % uid)
                json.append(string)
        if color == "all" and market_id is None:
            string = ("%s" % uid)
            json.append(string)
   
    no_cards = len(json)
    if no_cards == 0:
        return json
    print("Anzahl der Karten: %s" %len(json))
    #print(json)
    #print(json_dict)
    return json 

def transfer_cards(player, json, to):
    account = player
    acc = Account(account, steem_instance=stm)
    #json_dict = {"to":"urabutln","cards":["C1-37-K}
    if len(json) >= 50:
        start = 0
        end = 49
        i=1
        while end <= len(json):    
            
            new_json = json[start:end+1]
            #print("new",new_json)
            json_dict = {"to": to, "cards":new_json}
            stm.custom_json('sm_gift_cards', json_dict, required_posting_auths=[acc["name"]])    
            time.sleep(7)
            
            #print("Durchlauf %s %s " % (i,json_dict))
            start += 50
            if end == len(json):
                break
            elif (end +50) >= len(json):
                end = len(json)
            elif (end + 50) < len(json):
                end += 50
            i += 1
            json_dict.clear()
            
    elif len(json) < 50:
        json_dict = {"to": to, "cards":json}
        stm.custom_json('sm_gift_cards', json_dict, required_posting_auths=[acc["name"]])
        #print("ok", json_dict)
        
if __name__ == "__main__":
    #get_card_details()
    #check_decks()
    player = sys.argv[1]
    to = sys.argv[2]
    color = sys.argv[3]
    print("Transfer von: %s " % player)
    print("an: %s " % to)
    print("Farbe: %s " % color)
    ret = check_account(to)
    if ret == -1:
        print("Der Zielaccount existiert nicht, beende Transaktion")
    elif ret == 0:
        json1 = get_player_deck(player, color)
        print("Einzelkarten: %s" % json1)
        if len(json1) == 0:
            print("Nix zu tun, keine Karten gefunden")
        elif len(json1) > 0:
            transfer_cards(player, json1, to)
            #print("Länge der Custom Json Operation : %s" % (len(json1)*16))
            print("Transfer done")
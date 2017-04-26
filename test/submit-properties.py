#!/usr/bin/python
"""
This sample should ping ramco API for a changes in committee membership and post to a hyperledger blockchain.
David Conroy, 2017
"""
import config
import requests
from urllib import urlencode
import json
import base64
import logging
import sys
import os

# set up logging
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
ch.setFormatter(formatter)

root.addHandler(ch)
logging.basicConfig(level=logging.INFO)




# chaincode functions
def login_chain(enrollId, enrollSecret):

    payload = {"enrollId": enrollId,
               "enrollSecret": enrollSecret}
    r = requests.post(config.CORE_PEER_ADDRESS +
                      "/registrar", data=json.dumps(payload))

    return r.text


def query_thing(id):
    payload = {
        "jsonrpc": "2.0",
        "method": "query",
        "params": {
            "type": 1,
            "chaincodeID": {
                  "name": config.CHAINCODE_ID
            },
            "ctorMsg": {
                "function": "get_thing",
                "args": [
                    id
                ]
            },
            "secureContext": config.ENROLL_ID
        },
        "id": 1
    }

    r = requests.post(config.CORE_PEER_ADDRESS +
                      "/chaincode", data=json.dumps(payload))

    return r.json()


def does_thing_exist(id):
    results = query_thing(id)

    try:
        if (results["result"]["status"] == "OK"):
            return True
    except Exception as e:
        print(e)
        return False


def query_user(id):
    payload = {
        "jsonrpc": "2.0",
        "method": "query",
        "params": {
            "type": 1,
            "chaincodeID": {
                  "name": config.CHAINCODE_ID
            },
            "ctorMsg": {
                "function": "get_user",
                "args": [
                    id
                ]
            },
            "secureContext": config.ENROLL_ID
        },
        "id": 1
    }

    r = requests.post(config.CORE_PEER_ADDRESS +
                      "/chaincode", json.dumps(payload))

    return r.json()


def create_thing_in_chain(thing):
    thing = json.dumps(thing, ensure_ascii=False)
    logging.info(thing)
    payload = {
        "jsonrpc": "2.0",
        "method": "invoke",
        "params": {
            "type": 1,
            "chaincodeID": {
                "name": config.CHAINCODE_ID
            },
            "ctorMsg": {
                "function": "add_thing",
                "args": [
                    thing
                ]
            },
            "secureContext": config.ENROLL_ID
        },
        "id": 1
    }

    r = requests.post(config.CORE_PEER_ADDRESS + "/chaincode",
                      json.dumps(payload))

    return r.text


def create_if_doesnt_exist(property_data) :
    logging.info("Checking if "  + property_data["id"] +  "  exists on the Blockchain. ")
    if (does_thing_exist(property_data["id"])):
        logging.info("Existing Record - No changes made.")
    else:
        logging.info(property_data["id"] + " does not exist. Creating Blockchain Entry...")
        create_thing_in_chain(property_data)
    return True

def update_thing_in_chain(thing):
    payload = {
        "jsonrpc": "2.0",
        "method": "invoke",
        "params": {
            "type": 1,
            "chaincodeID": {
                "name": config.CHAINCODE_ID
            },
            "ctorMsg": {
                "function": "update_thing",
                "args": [
                    thing
                ]
            },
            "secureContext": config.ENROLL_ID
        },
        "id": 1
    }

    r = requests.post(config.CORE_PEER_ADDRESS + "/chaincode",
                      json.dumps(payload))

    return r.text


def main():
    logging.info('Started')
    login_chain(config.ENROLL_ID, config.ENROLL_SECRET)

    property_data = {}
    property_data2 = {}

    property_data["id"] = "US99999006038419"
    property_data["description"] = "1400 Main Street, Waltham, MA 02451"
    property_data["date"] = "1982"
    property_data["assoc_id"] = "1586"
    property_data["apn"] = "00"
    property_data["puid"] = "US99999006038419"
    property_data["parcel_id"] = "51122311"

    property_data2["id"] = "US88888006038419"
    property_data2["description"] = "256 Second Ave, Waltam, MA, 02451"
    property_data2["date"] = "1980"
    property_data2["assoc_id"] = "1586"
    property_data2["apn"] = "00"
    property_data2["puid"] = "US88888006038419"
    property_data2["parcel_id"] = "51122424"

    create_if_doesnt_exist(property_data)
    create_if_doesnt_exist(property_data2)



if __name__ == "__main__":
    main()

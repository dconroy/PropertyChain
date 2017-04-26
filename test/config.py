
#Association NRDS ID
ASSOC_NRDS = '0840'

ENROLL_ID = 'test_user0'
ENROLL_SECRET = 'MS9qrN8hFjlE'

with open('/Users/dconroy/Development/PropertyChain/blockchain/deployLocal/chaincode_id', 'r') as f:
    CHAINCODE_ID = f.readline()

#CHAINCODE_ID = '57eadf123218d8d699b42023a4ac77b5dc6c3dec663007844c9ccab6686509dc'
CORE_PEER_ADDRESS = 'http://localhost:7050'
#CORE_PEER_ADDRESS = 'http://d12a5c173c29437283c177a33d4088e6-vp0.us.blockchain.ibm.com:5004'

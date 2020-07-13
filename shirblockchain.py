import json
import hashlib
import sys
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request

class BlockChain():
    """ define a Block chain on one machine
    i have to define in other machine later 

    """
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # here for new block i use (1) andn for the first one proof is not matter so i use randomly for example 100
        self.new_block(prvious_hash=1, proof=100)

    def new_block(self, proof, prvious_hash=None):
        """ create a new block for our chain 

        constructor for the 'block' is :
        index: a unique ID for every block 
        timestamp: Time of generating a btransactionlock 
        transactions: List of Transactions is here 
        previous hash: in every new generating block we should put previous hash of that block 
        this is the one which make secure our block it means that if someone hack one block soe it means that he/she need to hack 
        every block after that block which they had hacked so it's make extremly hard to hack this is why block is so secure.

        PWO: proof of work --> in block chain we have prove of work it means that it will show that how hard you work and mine a block 
        which prove that you done a hard work so you have to have reward 
        i.e  for bitcoin in 2020 every block you mine you will get 6.25 bitcoin

        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            # the last one is soemhow tricky because we need prvious hash but for the initial block we don't have previous hash 
            # so i use a prameter by the name of prvious_hash = None 
            'previous_hash': prvious_hash or self.hash(self.chain[-1])
        }

        # so we created a block we should make sure that our mempool is empty so i will do it like this 
        self.current_transactions = []
        # i need to append the the new created block to our chian 
        self.chain.append(block)
        return block


    
    def new_transaction(self, sender, receiver, amount):
        """ ad a new transaction to the mempool
        in block chain you can not modify a block from everywhere, just you can apppend if you want to add a new block 
        """
        self.current_transactions.append({"sender": sender, "receiver":receiver, "amount": amount})

        return self.last_block['index']+1

    @staticmethod
    def hash(block):
        """ hash a block, in here i use sha-256 algor Algorithm, you can use different algorithms.

        # i will turn my block to a string with a json dump ---> in memory evrything when stored the ordring is not important
        # or sorting is not important, but in blockchain the ordring is imporant so i use ( sort_key=True)
        # encode is show that it will make a human readable 
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """ return the last block of block chain        """
        return self.chain[-1]
    
    @staticmethod
    def valid_proof(last_proof, proof):
        """ check if the proof is fine or not 
        for vallid_proof method we don't need self because i used @staticmethod
        """
        this_proof = f'{proof}{last_proof}'.encode()
        this_proof_hash = hashlib.sha256(this_proof).hexdigest()
        return this_proof_hash[:4] == '0000' #...............0000

    def proof_of_work(self, last_proof):
        """ show that the work is done and they perone work hard enough 
        in here our idea is that we asume the proof is (0)  and then calculate the hash of block, after that take sha256 algorithm
        if 4 last digit is become 0 like this ............0000 with our (0) proof we counted as signed block
        for ordinary computer it is very easy but if but if you wan to make it hard so try to use more zero ........0000000000 at the end     
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof
        

# here i use Flask instead of Django becausenew_i need just a restfull API so Flask is enough 
app = Flask(__name__)

# becuase i wanna make it on netwook so here i create a node_id 
node_id = str(uuid4())

blockchain = BlockChain()

@app.route("/mine", methods=["GET"])
def mine():
    """ this will mine one block and will added to the chain """
    # because we wanna start mining form last block so here we go 
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # after we find the last_proof so i need to add a coin to my self as a rewrad which you can see in bitcoin
    # in bitcoin before every 4 yeaer the amont of reward for every block will be haf 
    # it means that before 2002 it was 12.5, but after 2020 it is 6.25, intially for bitoin it was 50 coin for every block
    # here the sender is my self, and the recipient is also my self wich is my node_id

    blockchain.new_transaction(sender="0", receiver=node_id, amount=50)

    # right now i have added coin to my self so i need to create a block
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    response = {
        "message ": " new Block created ",
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"]
    }
    return jsonify(response), 200


@app.route("/transaction/new", methods=["POST"])
def new_transaction():
    """ i will add a new transaction 
    by getting sender , receiver and amount 
    """
    values = request.get_json()
    this_block = blockchain.new_transaction(values['sender'],values['receiver'], values['amount'])
    response = {"message": f"will be added to block {this_block}"}
    return jsonify(response), 201 # 201 means done
@app.route("/chain")
def full_chain():
    """ return the full chain"""
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain),
    }
    return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=sys.argv[1])
    
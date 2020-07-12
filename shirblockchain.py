import json
import hashlib
from flask import Flask
from time import time

class BlockChian():
    """ define a Block chain on one machine
    i have to define in other machine later 

    """
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # here for new block i use (1) andn for the first one proof is not matter so i use randomly for example 100
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, prvious_hash=None):
        """ create a new block for our chain 

        constructor for the 'block' is :
        index: a unique ID for every block 
        timestamp: Time of generating a block 
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
        self.chian.append(block)
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
        block_string = json.dumps(block, sort_key=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """ return the last block of block chain        """
        pass
    
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
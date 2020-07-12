class BlockChian():
    def __init__(self):
        self.chain = []
        self.current_transaction = []

    def new_block(self):
        """ create a new block for our chain 

        """
        pass
    
    def new_transaction(self):
        """ ad a new transaction to the mempool 

        """
        pass
    
    @classmethod
    def hash(block):
        """ hash a block, in here i use sha-256 algor Algorithm, you can use different algorithms.

        """
        pass
    
    @property
    def last_block(self):
        """ return the last block of block chain 

        """
        pass 
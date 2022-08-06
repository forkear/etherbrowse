import decimal
from typing import List, Tuple, Union
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.types import TxData, _Hash32, BlockData, BlockIdentifier, Wei

class MyService():
    
    def __init__(self, url:str):
        self.w3 = Web3(Web3.HTTPProvider(url))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    
    def get_transaction(self, tx: _Hash32 )  -> TxData:
        return self.w3.eth.get_transaction(tx)



    def get_addr(self, addr):
        if self.w3.isAddress(addr):
            return {'addr': addr, 'bln': self.get_balance(addr)}
        return None 


    def get_block(self, block_number: BlockIdentifier, full_transactions: bool = False) -> BlockData:
        return self.w3.eth.get_block(int(block_number)) 

    def get_transactions_from_blocks(self, blocks:List) -> List:
        transactions = []
        for block in blocks:
            for tx in block.transactions:
                    transaction = self.get_transaction(tx)
                    receipt = self.w3.eth.get_transaction_receipt(tx)
                    transactions.append((transaction,receipt))
        
        return transactions


    def get_last_transactions(self, count: int = 10) -> List:
        """
        insane
        """
        last = self.get_last_block_number()
        transactions = []
        while(last >= 0 and count >= 0 ):
            try:
                block = self.get_block(last, True)
                for tx in block.transactions:
                    transaction = self.get_transaction(tx)
                    transactions.append(transaction)
                    count=count-1

            except Exception as e:
                print(e)
            
            last = last - 1
        
        return transactions





        

    def get_blocks(self, page:int = 0, items_per_page:int = 10) -> Tuple[ int, int, int, int, int, List]:

        eth = self.w3.eth

        prev = next = last = first =  0

        last = eth.block_number
        first = int(last / items_per_page)

        if (page * items_per_page) > last:
            page = 0
        
        start = last - ( page * items_per_page )
        stop = start - items_per_page
        
        if page + 1 < first :
            prev = page + 1 
        
        if page - 1 >= 0:
            next = page - 1



        

        blocks = []

        for block_number in range(start, stop, -1):
            try:
                block = eth.get_block(block_number)
                blocks.append(block)
            except:
                print(f"ERROR: {block_number}")
                pass 

        return (page, prev, next, last, first, blocks)
    
    
    def get_last_block(self) -> BlockData:
        return self.w3.eth.get_block('latest')


    def get_last_block_number(self) -> int:
        return self.w3.eth.block_number
    
    def get_balance(self, address) ->  Union[int, decimal.Decimal]:

        try:
            address = self.w3.toChecksumAddress(address)
        except:
            return 0

        balance =   self.w3.eth.get_balance(address)

        ethers = self.w3.fromWei(balance, 'ether')

        return ethers
        
        

    

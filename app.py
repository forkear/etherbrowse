from xmlrpc.client import DateTime
import time
from flask import Flask, render_template, request, flash, redirect, url_for
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

import services

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'somerandomstring'

service = services.MyService(url=os.getenv("INFURA_URL"))


@app.context_processor
def get_last_block():
    return dict( get_last_block=service.get_last_block(), current_time= time.time())




@app.route("/search")
def search():
    query = request.args.get('query',None)
    if not query:
        return render_template('search.html', query=query, block=block, txn=txn)

    block = txn =  addr = None

    try:
        block = service.get_block(int(query))
    except:
        pass 

    try:
        txn = service.w3.eth.get_transaction(query)
    except:
        pass 


    try:
        addr =  service.get_addr(query)
    except:
        pass 

    return render_template('search.html', query=query, block=block, txn=txn, addr=addr)
    


@app.route("/")
def index():

    page = int(request.args.get('page', '0'))

    
    

    page, prev, next, last, first, latest_blocks = service.get_blocks(page)
    print(page)

    #latest_transactions = service.get_last_transactions(10)

    latest_transactions = service.get_transactions_from_blocks(latest_blocks)

    #flash('enviamos un mensaje')

    return render_template('index.html',
                           latest_blocks=latest_blocks,
                           page=page,
                           prev=prev,
                           next=next,
                           last=last,
                           first=first,
                           latest_transactions=latest_transactions)


@app.route("/address/<addr>")
def address(addr):
    balance = service.get_balance(addr)
    return render_template('address.html', address=addr, balance=balance)


@app.route("/block/<block_number>")
def block(block_number):
    block = service.get_block(int(block_number))
    datetime_block_str = datetime.fromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S')
                     
    print(block.transactions)
    txns = service.get_transactions_from_blocks([block])
    return render_template('block.html', block=block, txns=txns, datetime_block_str=datetime_block_str)


@app.route('/transaction/<hash>')
def transaction(hash):

    tx = service.w3.eth.get_transaction(hash)
    value = service.w3.fromWei(tx.value, 'ether')
    receipt = service.w3.eth.get_transaction_receipt(hash)
    gas_price = service.w3.fromWei(tx.gasPrice, 'ether')

    return render_template('transaction.html',
                           tx=tx,
                           value=value,
                           receipt=receipt,
                           gas_price=gas_price)


if __name__ == "__main__":
    app.run()

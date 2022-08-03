from xmlrpc.client import DateTime
import time
from flask import Flask, render_template, request, flash, redirect, url_for
import os
from datetime import datetime
from dotenv import load_dotenv
from forms import CodeForm, DeployForm
load_dotenv()

import services


app = Flask(__name__, template_folder="templates")

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response
app.wsgi_app = DispatcherMiddleware(
    Response('Not Found', status=404),
    {os.getenv("PREFIX_URL"): app.wsgi_app}
)


service = services.MyService(url=os.getenv("NODO_URL"))


@app.context_processor
def get_last_block():
    return dict( get_last_block=service.get_last_block(), current_time= time.time())



@app.route("/search")
def search():
    query = request.args.get('query',None)
    if not query:
        redirect(url_for('index'))

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

    latest_transactions = service.get_transactions_from_blocks(latest_blocks)

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




"""
https://web3py.readthedocs.io/en/latest/contracts.html
>>> from solcx import install_solc
>>> install_solc(version='latest')
"""

from solcx import compile_source

@app.route('/compiler', methods=['GET', 'POST'])
def compiler():
    bytecode =''
    abi = ''
    error = ''

    form = CodeForm(request.form)
    if request.method == 'POST':
        if form.validate():
            code = form.code.data 
            try:
                compiled_sol = compile_source(code, output_values=['abi', 'bin'])

                # retrieve the contract interface
                contract_id, contract_interface = compiled_sol.popitem()

                # get bytecode / bin
                bytecode = contract_interface['bin']

                # get abi
                abi =  contract_interface['abi']

                flash('Codigo compilado :-)')

            except Exception as e:
                error = f"{e}"
                error = error.replace('blackbox','username')
                

    return render_template('compiler.html', form=form, bytecode=bytecode, abi=abi, error=error)


@app.route('/compiler/deploy', methods=['GET', 'POST'])
def deploy_contract():
    form = DeployForm(request.form)
    if request.method == 'POST' and form.validate():
        pass

        
    return render_template('deploy.html')
    
    


"""
DEPLOY
# web3.py instance
>>> w3 = Web3(Web3.EthereumTesterProvider())

# set pre-funded account as sender
>>> w3.eth.default_account = w3.eth.accounts[0]

>>> Greeter = w3.eth.contract(abi=abi, bytecode=bytecode)

# Submit the transaction that deploys the contract
>>> tx_hash = Greeter.constructor().transact()

# Wait for the transaction to be mined, and get the transaction receipt


"""
if __name__ == "__main__":
    app.run()

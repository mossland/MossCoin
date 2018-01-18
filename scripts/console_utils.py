import pytest
import time
from populus.project import Project

proj = Project(project_dir='./')
password = 'testpass'

with proj.get_chain('rinkeby') as rinkeby:
    rw3 = rinkeby.web3
    rw3.personal.unlockAccount(rw3.eth.coinbase, password)

with proj.get_chain('local') as local:
    lw3 = local.web3

def coin(chain, force_deploy = False):
    total_supply = 250000000
    args = [total_supply]
    transaction = {
        'from' : chain.web3.eth.coinbase
    }

    if force_deploy:
        coin, _ = chain.provider.deploy_contract('MossCoin', deploy_args=args, deploy_transaction=transaction)
    else:
        coin, _ = chain.provider.get_or_deploy_contract('MossCoin', deploy_args=args, deploy_transaction=transaction)

    return coin

def get_account(chain, idx):
    w3 = chain.web3
    while len(w3.personal.listAccounts) <= idx:
        account = w3.personal.newAccount('testpass')
        w3.personal.unlockAccount(account, 'testpass')

    return w3.personal.listAccounts[idx]

def sendEther(chain, from_addr, to_addr, amount):
    w3 = chain.web3
    w3.eth.sendTransaction({'from':from_addr, 'to':to_addr 'value' : amount })

def crowdsale_pre(chain, period, cap, force_deploy = False):
    start = int(time.time()) + 60
    end = start + period
    moss_coin = coin(chain)
    coin_addr = moss_coin.address

    args = [start, end, 1, cap, 1, cap * 1000, chain.web3.eth.coinbase, coin_addr]

    transaction = {
        'from' : chain.web3.eth.coinbase
    }

    if force_deploy:
        contract, _ = chain.provider.deploy_contract('MossCrowdsalePre', deploy_args=args, deploy_transaction=transaction)
    else:
        contract, _ = chain.provider.get_or_deploy_contract('MossCrowdsalePre', deploy_args=args, deploy_transaction=transaction)

    moss_coin.transact({'from':chain.web3.eth.coinbase}).setCrowdsale(contract.address, True)

    return contract

def finney(amount):
    return amount * (10 ** 15)

def ether(amount):
    return amount * (10 ** 18)
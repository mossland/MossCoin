import pytest
from populus.project import Project

@pytest.fixture(scope='session')
def local_chain():
    proj = Project(project_dir='./')
    with proj.get_chain('local') as chain:
        yield chain

@pytest.fixture(scope='session')
def owner(local_chain):
    return local_chain.web3.eth.coinbase

@pytest.fixture(scope='session')
def moss_coin(local_chain, owner, total_supply):
    args = [total_supply]
    transaction = {
        'from' : owner
    }

    coin, _ = local_chain.provider.get_or_deploy_contract('MossCoin', deploy_args=args, deploy_transaction=transaction)

    return coin

@pytest.fixture(scope='session')
def local_accounts(local_chain):
    w3 = local_chain.web3
    while len(w3.personal.listAccounts) < 10:
        account = w3.personal.newAccount('testaccountpass')
        w3.personal.unlockAccount(account, 'testaccountpass')
    
    for account in w3.personal.listAccounts:
        if account == w3.eth.coinbase.lower():
            continue

        w3.eth.sendTransaction({'from':w3.eth.coinbase, 'to':account, 'value' : w3.toWei(100, 'ether') - w3.eth.getBalance(account) })

    return w3.personal.listAccounts

def deploy_crowdsale_pre(local_chain, owner, moss_coin, start, end, min_invest, max_invest, cap, rate):
    args = [start, end, rate, cap, min_invest, max_invest, coin_owner, moss_coin.address]

    transaction = {
        'from' : owner
    }

    contract, _ = local_chain.provider.deploy_contract('MossCrowdsalePre', deploy_args=args, deploy_transaction=transaction)
    moss_coin.transact({'from':coin_owner}).setCrowdsale(contract.address, True)

    return contract

def deploy_crowdsale_main(local_chain, owner, moss_coin, start, week, end, min_invest, max_invest, cap, rate):
    args = [start, start + week, start + week * 2, start + week * 3, end, rate, cap, min_invest, max_invest, coin_owner, moss_coin.address]

    transaction = {
        'from' : owner
    }

    contract, _ = local_chain.provider.deploy_contract('MossCrowdsaleMain', deploy_args=args, deploy_transaction=transaction)
    moss_coin.transact({'from':coin_owner}).setCrowdsale(contract.address, True)

    return contract
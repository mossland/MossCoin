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

def deploy_crowdsale(local_chain, owner, moss_coin, start, period, min_invest, max_invest, cap, rate):
    args = [start, end, rate, cap, min_invest, max_invest, coin_owner, moss_coin.address]

    transaction = {
        "from" : owner
    }

    contract, _ = local_chain.provider.deploy_contract('MossCrowdsale', deploy_args=args, deploy_transaction=transaction)
    moss_coin.transact({'from':coin_owner}).setCrowdsale(contract.address, True)

    return contract
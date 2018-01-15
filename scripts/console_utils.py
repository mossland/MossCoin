import pytest
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
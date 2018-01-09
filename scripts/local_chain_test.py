from populus.project import Project


total_supply = 30000000
proj = Project(project_dir='./')

with proj.get_chain('local') as chain:
    args = [total_supply]

    owner = chain.web3.eth.coinbase

    transaction = {
        'from' : owner
    }

    contract, _ = chain.provider.get_or_deploy_contract('MossCoin', deploy_args=args, deploy_transaction=transaction)
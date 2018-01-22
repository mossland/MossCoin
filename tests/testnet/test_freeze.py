import pytest
import web3.contract
from ethereum.tester import TransactionFailed

def test_freeze(chain, moss_coin, coin_owner, accounts):
    w3 = chain.web3
    now = chain.web3.eth.getBlock('latest').timestamp
    moss_coin.transact({'from':coin_owner}).freeze(accounts[1], now + 1000)

def test_freeze_fail(chain, moss_coin, coin_owner, accounts):
    w3 = chain.web3
    now = chain.web3.eth.getBlock('latest').timestamp

    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).freeze(accounts[1], now + 1000)

def test_freeze_transfer(chain, moss_coin, coin_owner, accounts):
    w3 = chain.web3
    now = chain.web3.eth.getBlock('latest').timestamp
    moss_coin.transact({'from':coin_owner}).freeze(accounts[1], now + 1000)
    moss_coin.transact({'from' : coin_owner}).transfer(accounts[1], 100)

    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from' : accounts[1]}).transfer(coin_owner, 100)

    while now + 1000 >= chain.web3.eth.getBlock('latest').timestamp:
        chain.rpc_methods.evm_mine()

    moss_coin.transact({'from' : accounts[1]}).transfer(coin_owner, 100)

def test_freeze_transfer_from(chain, moss_coin, coin_owner, accounts):
    w3 = chain.web3
    now = chain.web3.eth.getBlock('latest').timestamp
    moss_coin.transact({'from':coin_owner}).freeze(coin_owner, now + 1000)
    moss_coin.transact({'from':coin_owner}).approve(accounts[1], 100)

    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).transferFrom(coin_owner, accounts[2], 100)

    while now + 1000 >= chain.web3.eth.getBlock('latest').timestamp:
        chain.rpc_methods.evm_mine()

    moss_coin.transact({'from':accounts[1]}).transferFrom(coin_owner, accounts[2], 100)
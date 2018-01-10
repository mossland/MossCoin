import pytest
import web3.contract
from ethereum.tester import TransactionFailed

def test_upgrade(moss_coin, upgrade_target, coin_owner, accounts):
    moss_coin.transact({'from' : coin_owner}).transfer(accounts[1], 1000)

    moss_coin.transact({'from' : coin_owner}).setUpgradeAgent(upgrade_target.address)
    moss_coin.transact({'from' : accounts[1]}).upgrade(1000)

    assert upgrade_target.call().balanceOf(accounts[1]) == 1000

def test_upgrade_over(moss_coin, upgrade_target, coin_owner, accounts):
    moss_coin.transact({'from' : coin_owner}).transfer(accounts[1], 1000)

    moss_coin.transact({'from' : coin_owner}).setUpgradeAgent(upgrade_target.address)
    
    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from' : accounts[1]}).upgrade(1001)

    assert upgrade_target.call().balanceOf(accounts[1]) == 0

def test_upgrade_not_allowed(moss_coin, upgrade_target, coin_owner, accounts):
    moss_coin.transact({'from' : coin_owner}).transfer(accounts[1], 1000)

    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from' : accounts[1]}).setUpgradeAgent(upgrade_target.address)

    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from' : accounts[1]}).upgrade(1000)

    assert upgrade_target.call().balanceOf(accounts[1]) == 0

def test_upgrade_multi_set(moss_coin, upgrade_target, upgrade_target2, coin_owner, accounts):
    moss_coin.transact({'from' : coin_owner}).setUpgradeAgent(upgrade_target.address)

    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from' : coin_owner}).setUpgradeAgent(upgrade_target2.address)
    
    assert moss_coin.call().upgradeAgent().lower() == upgrade_target.address

def test_upgrade_over_supply(moss_coin, upgrade_target, coin_owner, accounts, total_supply, token_decimals):
    moss_coin.transact({'from' : coin_owner}).setUpgradeAgent(upgrade_target.address)

    moss_coin.transact({'from' : coin_owner}).upgrade(total_supply * (10 ** token_decimals))

    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from' : coin_owner}).upgrade(1)
    
    assert moss_coin.call().totalSupply() == 0
    assert upgrade_target.call().totalSupply() == total_supply * (10 ** token_decimals)
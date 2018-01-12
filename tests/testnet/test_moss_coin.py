import pytest
import web3.contract
from ethereum.tester import TransactionFailed

def test_token_initialized(moss_coin, coin_owner, token_symbol, token_name, token_decimals, total_supply, accounts):
    assert moss_coin.call().symbol() == token_symbol
    assert moss_coin.call().name() == token_name
    assert moss_coin.call().decimals() == token_decimals
    assert moss_coin.call().totalSupply() == (total_supply * (10 ** token_decimals))
    assert moss_coin.call().allowance(coin_owner, accounts[1]) == 0
    assert moss_coin.call().balanceOf(coin_owner) == (total_supply * (10 ** token_decimals))

def test_token_transfer(moss_coin, coin_owner, accounts):
    original = moss_coin.call().balanceOf(coin_owner)
    moss_coin.transact({'from' : coin_owner}).transfer(accounts[1], 100)

    assert moss_coin.call().balanceOf(accounts[1]) == 100
    assert moss_coin.call().balanceOf(coin_owner) == original - 100

def test_token_approval_allowance(moss_coin, coin_owner, accounts):
    moss_coin.transact({'from':coin_owner}).approve(accounts[1], 100)
    allowance = moss_coin.call().allowance(coin_owner, accounts[1])

    assert allowance == 100

def test_token_transfer_over_balance(moss_coin, coin_owner, accounts):
    original = moss_coin.call().balanceOf(coin_owner)

    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':coin_owner}).transfer(accounts[1], original + 1)
    
    assert moss_coin.call().balanceOf(coin_owner) == original

def test_token_transfer_from(moss_coin, coin_owner, accounts):
    original = moss_coin.call().balanceOf(coin_owner)
    moss_coin.transact({'from':coin_owner}).approve(accounts[1], 100)
    moss_coin.transact({'from':accounts[1]}).transferFrom(coin_owner, accounts[2], 100)

    assert moss_coin.call().balanceOf(coin_owner) == original - 100
    assert moss_coin.call().balanceOf(accounts[2]) == 100
    assert moss_coin.call().balanceOf(accounts[1]) == 0

def test_token_allowed_over(moss_coin, coin_owner, accounts):
    original = moss_coin.call().balanceOf(coin_owner)
    moss_coin.transact({'from':coin_owner}).approve(accounts[1], 99)

    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).transferFrom(coin_owner, accounts[2], 100)
    
    assert moss_coin.call().balanceOf(coin_owner) == original
    assert moss_coin.call().balanceOf(accounts[2]) == 0
    assert moss_coin.call().balanceOf(accounts[1]) == 0

def test_token_transfer_from_over_balance(moss_coin, coin_owner, accounts):
    original = moss_coin.call().balanceOf(coin_owner)
    moss_coin.transact({'from':coin_owner}).approve(accounts[1], original + 1)

    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).transferFrom(coin_owner, accounts[2], original + 1)

    assert moss_coin.call().balanceOf(coin_owner) == original
    assert moss_coin.call().balanceOf(accounts[2]) == 0
    assert moss_coin.call().balanceOf(accounts[1]) == 0

def test_token_transfer_zero_address(moss_coin, coin_owner, accounts):
    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':coin_owner}).transfer('0x0000000000000000000000000000000000000000', 100)

    moss_coin.transact({'from':coin_owner}).approve(accounts[1], 100)
    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).transferFrom(coin_owner, '0x0000000000000000000000000000000000000000', 100) 

def test_approve_change(moss_coin, coin_owner, accounts):
    moss_coin.transact({'from':coin_owner}).increaseApproval(accounts[1], 100)
    assert moss_coin.call().allowance(coin_owner, accounts[1]) == 100

    moss_coin.transact({'from':coin_owner}).decreaseApproval(accounts[1], 10)
    assert moss_coin.call().allowance(coin_owner, accounts[1]) == 90

def test_over_decrease(moss_coin, coin_owner, accounts):
    moss_coin.transact({'from':coin_owner}).approve(accounts[1], 100)
    moss_coin.transact({'from':coin_owner}).decreaseApproval(accounts[1], 110)

    assert moss_coin.call().allowance(coin_owner, accounts[1]) == 0
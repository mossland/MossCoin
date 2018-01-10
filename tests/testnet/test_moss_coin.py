import pytest
import web3.contract

def test_token_initialized(moss_coin, coin_owner, token_symbol, token_name, token_decimals, total_supply):
    assert moss_coin.call().symbol() == token_symbol
    assert moss_coin.call().name() == token_name
    assert moss_coin.call().decimals() == token_decimals
    assert moss_coin.call().totalSupply() == (total_supply * (10 ** token_decimals))
    assert moss_coin.call().balanceOf(coin_owner) == (total_supply * (10 ** token_decimals))

def test_token_transfer(moss_coin, coin_owner, accounts):
    original = moss_coin.call().balanceOf(coin_owner)
    moss_coin.transact({'from' : coin_owner}).transfer(accounts[1], 100)

    assert moss_coin.call().balanceOf(accounts[1]) == 100
    assert moss_coin.call().balanceOf(coin_owner) == original - 100
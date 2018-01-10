import pytest
import web3.contract
import web3.eth
import time
from ethereum.tester import TransactionFailed

def test_crowdsale_initialized(moss_crowdsale, moss_coin, coin_owner, period, min_invest, max_invest, cap, rate, token_decimals, invest_decimals):
    assert moss_crowdsale.call().endTime() - moss_crowdsale.call().startTime() == period
    assert moss_crowdsale.call().minInvest() == (min_invest * (10 ** invest_decimals))
    assert moss_crowdsale.call().maxInvest() == (max_invest * (10 ** invest_decimals))
    assert moss_crowdsale.call().cap() == (cap * (10 ** token_decimals))
    assert moss_crowdsale.call().weiRaised() == 0
    assert moss_crowdsale.call().token().lower() == moss_coin.address
    assert moss_crowdsale.call().wallet() == coin_owner

def test_crowdsale_buy(chain, moss_crowdsale, moss_coin, coin_owner, accounts, rate):
    w3 = chain.web3
    moss_crowdsale.transact({'from':accounts[1], 'value':w3.toWei(1,'ether')}).buyTokens(accounts[1])

    assert moss_coin.call().waiting(accounts[1]) == w3.toWei(1, 'ether') * rate

def test_crowdsale_buy_fallback(chain, moss_crowdsale, moss_coin, accounts, rate):
    w3 = chain.web3
    w3.eth.sendTransaction({'from':accounts[1], 'to':moss_crowdsale.address, 'value':w3.toWei(1,'ether')})
    assert moss_coin.call().waiting(accounts[1]) == w3.toWei(1, 'ether') * rate

def test_crowdsale_min_invest(chain, moss_crowdsale, moss_coin, accounts, min_invest, invest_decimals, rate):
    with pytest.raises(TransactionFailed):
        moss_crowdsale.transact({'from':accounts[1], 'value':min_invest * (10 ** invest_decimals) - 1}).buyTokens(accounts[1])

    assert moss_coin.call().waiting(accounts[1]) == 0

    moss_crowdsale.transact({'from':accounts[1], 'value':min_invest * (10 ** invest_decimals) }).buyTokens(accounts[1])
    assert moss_coin.call().waiting(accounts[1]) == min_invest * (10 ** invest_decimals)  * rate

def test_crowdsale_max_invest(chain, moss_crowdsale, moss_coin, accounts, min_invest, max_invest, invest_decimals, rate):
    with pytest.raises(TransactionFailed):
        moss_crowdsale.transact({'from':accounts[1], 'value':max_invest * (10 ** invest_decimals) + 1}).buyTokens(accounts[1])
    
    moss_crowdsale.transact({'from':accounts[2], 'value':(max_invest-min_invest) * (10 ** invest_decimals) + 1}).buyTokens(accounts[2])
    
    with pytest.raises(TransactionFailed):
        moss_crowdsale.transact({'from':accounts[2], 'value': min_invest * (10 ** invest_decimals)}).buyTokens(accounts[2])
    
    assert moss_coin.call().waiting(accounts[1]) == 0
    assert moss_coin.call().waiting(accounts[2]) == ((max_invest-min_invest) * (10 ** invest_decimals) + 1) * rate

def test_crowdsale_state_change(chain, moss_crowdsale, moss_coin, coin_owner, accounts, min_invest, invest_decimals):
    moss_coin.transact({'from':coin_owner}).setCrowdsale(moss_crowdsale.address, False)

    with pytest.raises(TransactionFailed):
        moss_crowdsale.transact({'from':accounts[1], 'value':min_invest * (10 ** invest_decimals) }).buyTokens(accounts[1])
    
    assert moss_coin.call().waiting(accounts[1]) == 0

def test_crowdsale_state_change_only_owner(chain, moss_crowdsale, moss_coin, accounts):
    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).setCrowdsale(moss_crowdsale.address, False)

    assert moss_coin.call().crowdsales(moss_crowdsale.address)
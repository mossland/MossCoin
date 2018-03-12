import pytest
import web3.contract
import web3.eth
import time
from ethereum.tester import TransactionFailed

@pytest.fixture
def bonus_time(ico_start, main_bonus_change_period, main_period):
    return [ico_start + main_bonus_change_period, ico_start + main_bonus_change_period * 2, ico_start + main_bonus_change_period * 3, ico_start + main_period + 1]

@pytest.fixture
def bonus_rate():
    return [1150, 1100, 1050, 1025]

def test_bonus_property(bonus_time, bonus_rate):
    assert len(bonus_time) == len(bonus_rate)

def test_bonus_rating(chain, bonus_time, bonus_rate, rate, ico_start, main_bonus_change_period):
    w3 = chain.web3
    assert token_amount(chain, 1 * w3.toWei(1, 'ether'), ico_start                                   , bonus_time, bonus_rate, rate) == 11500000000000000000000
    assert token_amount(chain, 1 * w3.toWei(1, 'ether'), ico_start + main_bonus_change_period - 1    , bonus_time, bonus_rate, rate) == 11500000000000000000000
    assert token_amount(chain, 1 * w3.toWei(1, 'ether'), ico_start + main_bonus_change_period        , bonus_time, bonus_rate, rate) == 11000000000000000000000
    assert token_amount(chain, 1 * w3.toWei(1, 'ether'), ico_start + main_bonus_change_period * 2 - 1, bonus_time, bonus_rate, rate) == 11000000000000000000000
    assert token_amount(chain, 1 * w3.toWei(1, 'ether'), ico_start + main_bonus_change_period * 2    , bonus_time, bonus_rate, rate) == 10500000000000000000000
    assert token_amount(chain, 1 * w3.toWei(1, 'ether'), ico_start + main_bonus_change_period * 3 - 1, bonus_time, bonus_rate, rate) == 10500000000000000000000
    assert token_amount(chain, 1 * w3.toWei(1, 'ether'), ico_start + main_bonus_change_period * 3    , bonus_time, bonus_rate, rate) == 10250000000000000000000
    assert token_amount(chain, 1 * w3.toWei(1, 'ether'), ico_start + main_bonus_change_period * 4 - 1, bonus_time, bonus_rate, rate) == 10250000000000000000000

def bonus(chain, buy_time, bonus_time, bonus_rate):
    for i in range(0, 4):
        if buy_time < bonus_time[i]:
            return bonus_rate[i]

def token_amount(chain, wei, buy_time, bonus_time, bonus_rate, rate):
    return wei * rate * bonus(chain, buy_time, bonus_time, bonus_rate) // 1000

def test_crowdsale_initialized(chain, moss_crowdsale, moss_coin, coin_owner, main_period, min_invest, cap_main, rate, token_decimals, invest_decimals, bonus_time, bonus_rate):
    w3 = chain.web3
    assert moss_crowdsale.call().endTime() - moss_crowdsale.call().startTime() == main_period
    assert moss_crowdsale.call().minInvest() == (min_invest * (10 ** invest_decimals))
    assert moss_crowdsale.call().cap() == (cap_main * (10 ** token_decimals))
    assert moss_crowdsale.call().token().lower() == moss_coin.address

    for i in range(0, len(bonus_time)):
        assert moss_crowdsale.call().ends(i) == bonus_time[i]
    
    for i in range(0, len(bonus_rate)):
        assert moss_crowdsale.call().bonus(i) == bonus_rate[i]

def test_crowdsale_buy(chain, moss_crowdsale, moss_coin, coin_owner, accounts, rate, bonus_time, bonus_rate, ico_start):
    w3 = chain.web3
    moss_crowdsale.transact({'from':accounts[1], 'value':w3.toWei(1,'ether')}).buyTokens(accounts[1])

    assert moss_coin.call().waiting(accounts[1]) == token_amount(chain, w3.toWei(1,'ether'), ico_start, bonus_time, bonus_rate, rate)

def test_crowdsale_buy_fallback(chain, moss_crowdsale, moss_coin, accounts, rate, bonus_time, bonus_rate, ico_start):
    w3 = chain.web3
    w3.eth.sendTransaction({'from':accounts[1], 'to':moss_crowdsale.address, 'value':w3.toWei(1,'ether')})
    assert moss_coin.call().waiting(accounts[1]) == token_amount(chain, w3.toWei(1,'ether'), ico_start, bonus_time, bonus_rate, rate)

def test_crowdsale_min_invest(chain, moss_crowdsale, moss_coin, accounts, min_invest, invest_decimals, rate, bonus_time, bonus_rate, ico_start):
    with pytest.raises(TransactionFailed):
        moss_crowdsale.transact({'from':accounts[1], 'value':min_invest * (10 ** invest_decimals) - 1}).buyTokens(accounts[1])

    assert moss_coin.call().waiting(accounts[1]) == 0

    moss_crowdsale.transact({'from':accounts[1], 'value':min_invest * (10 ** invest_decimals) }).buyTokens(accounts[1])
    assert moss_coin.call().waiting(accounts[1]) == token_amount(chain, min_invest * (10 ** invest_decimals), ico_start, bonus_time, bonus_rate, rate)

def test_crowdsale_state_change(chain, moss_crowdsale, test_crowdsale, moss_coin, coin_owner, accounts, min_invest, invest_decimals):
    moss_coin.transact({'from':coin_owner}).setCrowdsale(test_crowdsale.address)

    with pytest.raises(TransactionFailed):
        moss_crowdsale.transact({'from':accounts[1], 'value':min_invest * (10 ** invest_decimals) }).buyTokens(accounts[1])
    
    assert moss_coin.call().waiting(accounts[1]) == 0

def test_crowdsale_state_change_only_owner(chain, moss_crowdsale, test_crowdsale, moss_coin, accounts):
    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).setCrowdsale(test_crowdsale.address)

    assert moss_coin.call().crowdsale().lower() == moss_crowdsale.address

def test_crowdsale_release(chain, moss_crowdsale, moss_coin, coin_owner, accounts, rate, bonus_time, bonus_rate, ico_start):
    w3 = chain.web3
    moss_crowdsale.transact({'from':accounts[1], 'value':w3.toWei(1,'ether')}).buyTokens(accounts[1])
    moss_coin.transact({'from':coin_owner}).release(accounts[1])

    assert moss_coin.call().saled() == token_amount(chain, w3.toWei(1,'ether'), ico_start, bonus_time, bonus_rate, rate)
    assert moss_coin.call().waiting(accounts[1]) == 0
    assert moss_coin.call().balanceOf(accounts[1]) == token_amount(chain, w3.toWei(1,'ether'), ico_start, bonus_time, bonus_rate, rate)

def test_crowdsale_release_only_owner(chain, moss_crowdsale, moss_coin, coin_owner, accounts, rate, bonus_time, bonus_rate, ico_start):
    w3 = chain.web3
    moss_crowdsale.transact({'from':accounts[1], 'value':w3.toWei(1,'ether')}).buyTokens(accounts[1])

    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).release(accounts[1])

    assert moss_coin.call().saled() == token_amount(chain, w3.toWei(1,'ether'), ico_start, bonus_time, bonus_rate, rate)
    assert moss_coin.call().waiting(accounts[1]) == token_amount(chain, w3.toWei(1,'ether'), ico_start, bonus_time, bonus_rate, rate)
    assert moss_coin.call().balanceOf(accounts[1]) == 0

def test_crowdsale_reject(chain, moss_crowdsale, moss_coin, coin_owner, accounts, rate, bonus_time, bonus_rate):
    w3 = chain.web3
    moss_crowdsale.transact({'from':accounts[1], 'value':w3.toWei(1,'ether')}).buyTokens(accounts[1])
    moss_coin.transact({'from':coin_owner}).reject(accounts[1])

    assert moss_coin.call().waiting(accounts[1]) == 0
    assert moss_coin.call().balanceOf(accounts[1]) == 0
    assert moss_coin.call().saled() == 0

def test_crowdsale_reject_only_owner(chain, moss_crowdsale, moss_coin, coin_owner, accounts, rate, bonus_time, bonus_rate, ico_start):
    w3 = chain.web3
    moss_crowdsale.transact({'from':accounts[1], 'value':w3.toWei(1,'ether')}).buyTokens(accounts[1])

    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).reject(accounts[1])

    assert moss_coin.call().saled() == token_amount(chain, w3.toWei(1,'ether'), ico_start, bonus_time, bonus_rate, rate)
    assert moss_coin.call().waiting(accounts[1]) == token_amount(chain, w3.toWei(1,'ether'), ico_start, bonus_time, bonus_rate, rate)
    assert moss_coin.call().balanceOf(accounts[1]) == 0


# bonus rating test
def test_crowdsale_bonus_rating(chain, moss_crowdsale, moss_coin, coin_owner, accounts, rate, bonus_time, bonus_rate):
    w3 = chain.web3
    for criteria in bonus_time[:-1]:
        while criteria >= chain.web3.eth.getBlock('latest').timestamp:
            chain.rpc_methods.evm_mine()
        
        balance = moss_coin.call().waiting(accounts[1])
        moss_crowdsale.transact({'from':accounts[1], 'value' : w3.toWei(1,'ether')}).buyTokens(accounts[1])
        assert moss_coin.call().waiting(accounts[1]) == balance + token_amount(chain, w3.toWei(1,'ether'), chain.web3.eth.getBlock('latest').timestamp, bonus_time, bonus_rate, rate)

def test_after_crowdsale_end(chain, moss_crowdsale, moss_coin, coin_owner, accounts, rate):
    w3 = chain.web3
    while moss_crowdsale.call().endTime() >= chain.web3.eth.getBlock('latest').timestamp:
        chain.rpc_methods.evm_mine()

    with pytest.raises(TransactionFailed):
        moss_crowdsale.transact({'from':accounts[1], 'value':w3.toWei(1,'ether')}).buyTokens(accounts[1])
    
    assert moss_coin.call().waiting(accounts[1]) == 0

def test_over_cap(chain, moss_crowdsale, moss_coin, coin_owner, accounts, rate, cap_main, token_decimals):
    w3 = chain.web3
    moss_crowdsale.transact({'from':accounts[1], 'value': cap_main // (rate * 2) * (10 ** token_decimals)}).buyTokens(accounts[1])

    with pytest.raises(TransactionFailed):
        moss_crowdsale.transact({'from':accounts[4], 'value': cap_main // (rate * 2) * (10 ** token_decimals)}).buyTokens(accounts[4])

    moss_coin.transact({'from':coin_owner}).reject(accounts[1])
    moss_crowdsale.transact({'from':accounts[4], 'value': cap_main // (rate * 2) * (10 ** token_decimals)}).buyTokens(accounts[4])

def test_change_rate(chain, moss_crowdsale, coin_owner):
    moss_crowdsale.transact({'from':coin_owner}).changeRate(1000)

    assert moss_crowdsale.call().rate() == 1000

def test_change_rate_owner_only(chain, moss_crowdsale, accounts, rate):
    with pytest.raises(TransactionFailed):
        moss_crowdsale.transact({'from':accounts[1]}).changeRate(1000)
    
    assert moss_crowdsale.call().rate() == rate
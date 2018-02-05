import pytest
import web3.contract
import web3.eth
import time
from ethereum.tester import TransactionFailed

@pytest.fixture
def bonus_ether():
    return [500, 3000, 4000, 5000]

@pytest.fixture
def bonus_rate():
    return [ [1150, 1250, 1350, 1450, 1550]
           , [1100, 1200, 1300, 1450, 1550]
           , [1050, 1150, 1250, 1450, 1550]
           , [1025, 1100, 1200, 1450, 1550] ]

def test_bonus_property(bonus_ether, bonus_rate):
    for rate in bonus_rate:
        assert len(bonus_ether) + 1 == len(rate)

def sale_bonus(chain, wei, now, bonus_ether, bonus_rate, start, main_bonus_change_period):
    period_idx = -1
    
    for j in range(1, 4):
        if now < start + j * main_bonus_change_period:
            period_idx = j - 1
            break
    
    if period_idx == -1:
        period_idx = 3

    for i in range(0, 4):
        if wei < bonus_ether[i] * chain.web3.toWei(1,'ether'):
            return bonus_rate[period_idx][i]
    
    return bonus_rate[period_idx][-1]

def token_amount(chain, wei, now, bonus_ether, bonus_rate, rate, start, main_bonus_change_period):
    return wei * rate * sale_bonus(chain, wei, now, bonus_ether, bonus_rate, start, main_bonus_change_period) // 1000

def test_main_bonus_rating(chain, bonus_ether, bonus_rate, rate, testernet_start, main_period, main_bonus_change_period):
    w3 = chain.web3
    start = testernet_start
    end = testernet_start + main_period

    # 1st week
    week1end = start + main_bonus_change_period - 1

    assert token_amount(chain, 500 * w3.toWei(1, 'ether') - 1,  week1end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 5750000000000000000000000 - 11500
    assert token_amount(chain, 500 * w3.toWei(1, 'ether'),      week1end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 6250000000000000000000000
    assert token_amount(chain, 3000 * w3.toWei(1, 'ether') - 1, week1end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 37500000000000000000000000 - 12500
    assert token_amount(chain, 3000 * w3.toWei(1, 'ether'),     week1end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 40500000000000000000000000
    assert token_amount(chain, 4000 * w3.toWei(1, 'ether') - 1, week1end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 54000000000000000000000000 - 13500
    assert token_amount(chain, 4000 * w3.toWei(1, 'ether'),     week1end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 58000000000000000000000000
    assert token_amount(chain, 5000 * w3.toWei(1, 'ether') - 1, week1end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 72500000000000000000000000 - 14500
    assert token_amount(chain, 5000 * w3.toWei(1, 'ether'),     week1end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 77500000000000000000000000
    
    # 2nd week
    week2start = start + main_bonus_change_period
    week2end = start + 2 * main_bonus_change_period - 1

    assert token_amount(chain, 500 * w3.toWei(1, 'ether') - 1,  week2start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 5500000000000000000000000 - 11000
    assert token_amount(chain, 500 * w3.toWei(1, 'ether'),      week2start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 6000000000000000000000000
    assert token_amount(chain, 3000 * w3.toWei(1, 'ether') - 1, week2start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 36000000000000000000000000 - 12000
    assert token_amount(chain, 3000 * w3.toWei(1, 'ether'),     week2start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 39000000000000000000000000
    assert token_amount(chain, 4000 * w3.toWei(1, 'ether') - 1, week2start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 52000000000000000000000000 - 13000
    assert token_amount(chain, 4000 * w3.toWei(1, 'ether'),     week2start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 58000000000000000000000000
    assert token_amount(chain, 5000 * w3.toWei(1, 'ether') - 1, week2start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 72500000000000000000000000 - 14500
    assert token_amount(chain, 5000 * w3.toWei(1, 'ether'),     week2start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 77500000000000000000000000

    assert token_amount(chain, 500 * w3.toWei(1, 'ether') - 1,  week2end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 5500000000000000000000000 - 11000
    assert token_amount(chain, 500 * w3.toWei(1, 'ether'),      week2end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 6000000000000000000000000
    assert token_amount(chain, 3000 * w3.toWei(1, 'ether') - 1, week2end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 36000000000000000000000000 - 12000
    assert token_amount(chain, 3000 * w3.toWei(1, 'ether'),     week2end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 39000000000000000000000000
    assert token_amount(chain, 4000 * w3.toWei(1, 'ether') - 1, week2end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 52000000000000000000000000 - 13000
    assert token_amount(chain, 4000 * w3.toWei(1, 'ether'),     week2end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 58000000000000000000000000
    assert token_amount(chain, 5000 * w3.toWei(1, 'ether') - 1, week2end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 72500000000000000000000000 - 14500
    assert token_amount(chain, 5000 * w3.toWei(1, 'ether'),     week2end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 77500000000000000000000000
    
    # 3rd week
    week3start = start + 2 * main_bonus_change_period
    week3end = start + 3 * main_bonus_change_period - 1

    assert token_amount(chain, 500 * w3.toWei(1, 'ether') - 1,  week3start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 5250000000000000000000000 - 10500
    assert token_amount(chain, 500 * w3.toWei(1, 'ether'),      week3start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 5750000000000000000000000
    assert token_amount(chain, 3000 * w3.toWei(1, 'ether') - 1, week3start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 34500000000000000000000000 - 11500
    assert token_amount(chain, 3000 * w3.toWei(1, 'ether'),     week3start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 37500000000000000000000000
    assert token_amount(chain, 4000 * w3.toWei(1, 'ether') - 1, week3start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 50000000000000000000000000 - 12500
    assert token_amount(chain, 4000 * w3.toWei(1, 'ether'),     week3start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 58000000000000000000000000
    assert token_amount(chain, 5000 * w3.toWei(1, 'ether') - 1, week3start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 72500000000000000000000000 - 14500
    assert token_amount(chain, 5000 * w3.toWei(1, 'ether'),     week3start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 77500000000000000000000000

    assert token_amount(chain, 500 * w3.toWei(1, 'ether') - 1,  week3end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 5250000000000000000000000 - 10500
    assert token_amount(chain, 500 * w3.toWei(1, 'ether'),      week3end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 5750000000000000000000000
    assert token_amount(chain, 3000 * w3.toWei(1, 'ether') - 1, week3end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 34500000000000000000000000 - 11500
    assert token_amount(chain, 3000 * w3.toWei(1, 'ether'),     week3end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 37500000000000000000000000
    assert token_amount(chain, 4000 * w3.toWei(1, 'ether') - 1, week3end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 50000000000000000000000000 - 12500
    assert token_amount(chain, 4000 * w3.toWei(1, 'ether'),     week3end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 58000000000000000000000000
    assert token_amount(chain, 5000 * w3.toWei(1, 'ether') - 1, week3end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 72500000000000000000000000 - 14500
    assert token_amount(chain, 5000 * w3.toWei(1, 'ether'),     week3end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 77500000000000000000000000

    # 4th week
    week4start = start + 3 * main_bonus_change_period
    week4end = end

    assert token_amount(chain, 500 * w3.toWei(1, 'ether') - 1,  week4start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 5125000000000000000000000 - 10250
    assert token_amount(chain, 500 * w3.toWei(1, 'ether'),      week4start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 5500000000000000000000000
    assert token_amount(chain, 3000 * w3.toWei(1, 'ether') - 1, week4start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 33000000000000000000000000 - 11000
    assert token_amount(chain, 3000 * w3.toWei(1, 'ether'),     week4start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 36000000000000000000000000
    assert token_amount(chain, 4000 * w3.toWei(1, 'ether') - 1, week4start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 48000000000000000000000000 - 12000
    assert token_amount(chain, 4000 * w3.toWei(1, 'ether'),     week4start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 58000000000000000000000000
    assert token_amount(chain, 5000 * w3.toWei(1, 'ether') - 1, week4start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 72500000000000000000000000 - 14500
    assert token_amount(chain, 5000 * w3.toWei(1, 'ether'),     week4start, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 77500000000000000000000000

    assert token_amount(chain, 500 * w3.toWei(1, 'ether') - 1,  week4end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 5125000000000000000000000 - 10250
    assert token_amount(chain, 500 * w3.toWei(1, 'ether'),      week4end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 5500000000000000000000000
    assert token_amount(chain, 3000 * w3.toWei(1, 'ether') - 1, week4end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 33000000000000000000000000 - 11000
    assert token_amount(chain, 3000 * w3.toWei(1, 'ether'),     week4end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 36000000000000000000000000
    assert token_amount(chain, 4000 * w3.toWei(1, 'ether') - 1, week4end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 48000000000000000000000000 - 12000
    assert token_amount(chain, 4000 * w3.toWei(1, 'ether'),     week4end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 58000000000000000000000000
    assert token_amount(chain, 5000 * w3.toWei(1, 'ether') - 1, week4end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 72500000000000000000000000 - 14500
    assert token_amount(chain, 5000 * w3.toWei(1, 'ether'),     week4end, bonus_ether, bonus_rate, rate, start, main_bonus_change_period) == 77500000000000000000000000

def test_main_crowdsale_initialized(chain, moss_crowdsale_main, moss_coin, coin_owner, main_period, min_invest, cap_main, rate, token_decimals, invest_decimals, bonus_ether, bonus_rate, main_bonus_change_period):
    w3 = chain.web3
    assert moss_crowdsale_main.call().endTime() - moss_crowdsale_main.call().startTime() == main_period
    assert moss_crowdsale_main.call().minInvest() == (min_invest * (10 ** invest_decimals))
    assert moss_crowdsale_main.call().cap() == (cap_main * (10 ** token_decimals))
    assert moss_crowdsale_main.call().token().lower() == moss_coin.address

    for i in range(0, len(bonus_ether)):
        assert moss_crowdsale_main.call().values(i) == bonus_ether[i] * w3.toWei(1, 'ether')
    
    for i in range(0, len(bonus_rate)):
        for j in range(0, len(bonus_rate[i])):
            assert moss_crowdsale_main.call().bonus(i, j) == bonus_rate[i][j]

    assert moss_crowdsale_main.call().ends(0) == moss_crowdsale_main.call().startTime() + main_bonus_change_period
    assert moss_crowdsale_main.call().ends(1) == moss_crowdsale_main.call().startTime() + main_bonus_change_period * 2
    assert moss_crowdsale_main.call().ends(2) == moss_crowdsale_main.call().startTime() + main_bonus_change_period * 3
    assert moss_crowdsale_main.call().ends(3) == moss_crowdsale_main.call().endTime() + 1

def test_main_crowdsale_buy(chain, moss_crowdsale_main, moss_coin, testernet_start, main_bonus_change_period, coin_owner, accounts, rate, bonus_ether, bonus_rate):
    w3 = chain.web3
    moss_crowdsale_main.transact({'from':accounts[1], 'value':w3.toWei(1,'ether')}).buyTokens(accounts[1])

    assert moss_coin.call().waiting(accounts[1]) == token_amount(chain, w3.toWei(1,'ether'), testernet_start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period)

def test_main_crowdsale_buy_fallback(chain, moss_crowdsale_main, moss_coin, testernet_start, main_bonus_change_period, accounts, rate, bonus_ether, bonus_rate):
    w3 = chain.web3
    w3.eth.sendTransaction({'from':accounts[1], 'to':moss_crowdsale_main.address, 'value':w3.toWei(1,'ether')})
    assert moss_coin.call().waiting(accounts[1]) == token_amount(chain, w3.toWei(1,'ether'), testernet_start, bonus_ether, bonus_rate, rate,testernet_start, main_bonus_change_period)

def test_main_crowdsale_min_invest(chain, moss_crowdsale_main, moss_coin, testernet_start, main_bonus_change_period, accounts, min_invest, invest_decimals, rate, bonus_ether, bonus_rate):
    with pytest.raises(TransactionFailed):
        moss_crowdsale_main.transact({'from':accounts[1], 'value':min_invest * (10 ** invest_decimals) - 1}).buyTokens(accounts[1])

    assert moss_coin.call().waiting(accounts[1]) == 0

    moss_crowdsale_main.transact({'from':accounts[1], 'value':min_invest * (10 ** invest_decimals) }).buyTokens(accounts[1])
    assert moss_coin.call().waiting(accounts[1]) == token_amount(chain, min_invest * (10 ** invest_decimals), testernet_start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period)

def test_main_crowdsale_state_change(chain, moss_crowdsale_main, test_crowdsale, moss_coin, coin_owner, accounts, min_invest, invest_decimals):
    moss_coin.transact({'from':coin_owner}).setCrowdsale(test_crowdsale.address)

    with pytest.raises(TransactionFailed):
        moss_crowdsale_main.transact({'from':accounts[1], 'value':min_invest * (10 ** invest_decimals) }).buyTokens(accounts[1])
    
    assert moss_coin.call().waiting(accounts[1]) == 0

def test_main_crowdsale_state_change_only_owner(chain, moss_crowdsale_main, test_crowdsale, moss_coin, accounts):
    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).setCrowdsale(test_crowdsale.address)

    assert moss_coin.call().crowdsale().lower() == moss_crowdsale_main.address

def test_main_crowdsale_release(chain, moss_crowdsale_main, moss_coin, coin_owner, testernet_start, main_bonus_change_period, accounts, rate, bonus_ether, bonus_rate):
    w3 = chain.web3
    moss_crowdsale_main.transact({'from':accounts[1], 'value':w3.toWei(1,'ether')}).buyTokens(accounts[1])
    moss_coin.transact({'from':coin_owner}).release(accounts[1])

    assert moss_coin.call().balanceOf(accounts[1]) == token_amount(chain, w3.toWei(1,'ether'), testernet_start, bonus_ether, bonus_rate, rate, testernet_start, main_bonus_change_period)

def test_main_crowdsale_release_only_owner(chain, moss_crowdsale_main, moss_coin, coin_owner, accounts, rate):
    w3 = chain.web3
    moss_crowdsale_main.transact({'from':accounts[1], 'value':w3.toWei(1,'ether')}).buyTokens(accounts[1])

    with pytest.raises(TransactionFailed):
        moss_coin.transact({'from':accounts[1]}).release(accounts[1])

    assert moss_coin.call().balanceOf(accounts[1]) == 0

# bonus rating test
def test_main_crowdsale_bonus_rating(chain, moss_crowdsale_main, moss_coin, coin_owner, main_period, main_bonus_change_period, accounts, rate, bonus_ether, bonus_rate):
    w3 = chain.web3

    start = moss_crowdsale_main.call().startTime()
    buy_time = [ start
               , start + main_bonus_change_period - 1
               , start + main_bonus_change_period
               , start + 2 * main_bonus_change_period - 1
               , start + 2 * main_bonus_change_period
               , start + 3 * main_bonus_change_period - 1
               , start + 3 * main_bonus_change_period
               , moss_crowdsale_main.call().endTime() ]

    for time in buy_time:
        for criteria in bonus_ether:
            tokens = moss_crowdsale_main.call().getTokens(w3.toWei(1, 'ether') * criteria - 1, time)
            assert tokens == token_amount(chain, w3.toWei(1,'ether') * criteria - 1, time, bonus_ether, bonus_rate, rate, start, main_bonus_change_period)
            
            tokens = moss_crowdsale_main.call().getTokens(w3.toWei(1, 'ether') * criteria, time)
            assert tokens == token_amount(chain, w3.toWei(1,'ether') * criteria, time, bonus_ether, bonus_rate, rate, start, main_bonus_change_period)
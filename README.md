<p align="center"> <img src="/img/logo.png"> </p>
<p align="center">
  <img src="https://travis-ci.org/realityreflection/MossCoin.svg?branch=master">
  <a href="http://t.me/mossland">
    <img src="https://img.shields.io/badge/telegram-kor-brightgreen.svg" alt="chat on telegram(kor)">
  </a>
  <a href="http://t.me/mossland_eng">
    <img src="https://img.shields.io/badge/telegram-eng-green.svg" alt="chat on telegram(eng)">
  </a>
  <a href="https://twitter.com/intent/follow?screen_name=TheMossLand">
    <img src="https://img.shields.io/twitter/follow/TheMossLand.svg?style=social&label=Follow" alt="follow on Twitter">
  </a>
</p>

## Requirements
- OSX or linux
- [python3](https://www.python.org)
- [solc](http://solidity.readthedocs.io/en/latest/installing-solidity.html)
- [populus](https://github.com/ethereum/populus)

## Contracts
MossCoin is a token which is based on Zepplin StandardToken ERC-20 contract.

If you want to know more detailed information about this project, visit our [website](http://moss.land)

## Installation

1. Install [python3](https://www.python.org) and [solc](http://solidity.readthedocs.io/en/latest/installing-solidity.html). follow install instruction on link.

2. Initialize development environment. Execute the command below. 
```
git clone --recursive git@github.com:MossCoin/MossCoin.git
cd MossCoin
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip3 install -r requirements.txt
```

3. Test solc and populus are correctly installed:
```
$ solc --version
solc, the solidity compiler commandline interface
Version: 0.4.19+commit.c4cbbb05.linux.g++
populus
Usage: populus [OPTIONS] COMMAND [ARGS]...

  Populus

Options:
  ...
```

4. Then, initialize private block chain for test:
```
bash scripts/init_local_chain.sh
```

## Compile

You can compile solidity code by using `populus compile` command. Compile results are saved in `build/contracts.json`.

## Test

If you want to test basic functionalities only, run `py.test tests/testnet`.

To test deploying token and more complexed functionalities, you need local private chain.

First, run local private chain by using the command below:

```
/chains/local/./run_chain.sh
```

Then, open another terminal and run test by using the command below:

```
py.test tests/localnet
```

<p align="center"> <img src="/img/image.png"> </p>

## Requirements
- OSX or linux
- [python3](www.python.org)
- [solc](solidity.readthedocs.io/en/latest/installing-solidity.html)
- [populus](github.com/ethereum/populus)

## Contracts
MossCoin is based on Zepplin StandardToken ERC-20 contract.

if you want to know detail information about this project, see our [white paper](moss.land)

## Installation

1. install [python3](www.python.org) and [solc](solidity.readthedocs.io/en/latest/installing-solidity.html). follow install instruction on link.

2. initialize development environment. execute bellow commands on terimal.
```
git clone --recursive git@github.com:MossCoin/MossCoin.git
cd MossCoin
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip3 install -r requirements.txt
``` 

3. test solc and populus are correctly installed:
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

4. then, initialize private block chain for test:
```
bash scripts/init_local_chain.sh
```

## Compile

you can compile solidity code by using `populus compile` command. compile results are saved in `build/contracts.json`.

## Test

if you want to test basic functionality, run `py.test tests/testnet`.

for test deploying token and more complex functionality, using local private chain.

first, run local private chain:

```
/chains/local/./run_chain.sh
```

then, open another terminal and run test:

```
py.test tests/localnet
```
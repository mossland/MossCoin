<p align="center"> <img src="/img/logo.png"> </p>

## Requirements
- OSX or linux
- [python3](www.python.org)
- [solc](solidity.readthedocs.io/en/latest/installing-solidity.html)
- [populus](github.com/ethereum/populus)

## Contracts
MossCoin is a token which is based on Zepplin StandardToken ERC-20 contract.

If you want to know more detailed information about this project, visit our [website](http://moss.land)

## Installation

1. Install [python3](www.python.org) and [solc](solidity.readthedocs.io/en/latest/installing-solidity.html). follow install instruction on link.

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
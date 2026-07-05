<p align="center"> <img src="/img/logo.png"> </p>
<p align="center">
  <a href="https://twitter.com/intent/follow?screen_name=TheMossLand">
    <img src="https://img.shields.io/twitter/follow/TheMossLand.svg?style=social&label=Follow" alt="follow on Twitter">
  </a>
</p>

---
📌 **Deprecation Notice — this is the legacy 2018 ERC-20 (do not use)**

This repository holds the **original 2018 ERC-20 MossCoin (MOC)** and is **deprecated**. The current, official MOC is the **2025 Ethereum mainnet ERC-20**:

- **Current MOC (2025 ERC-20):** [`0x8bbfe65e31b348cd823c62e02ad8c19a84dd0dab`](https://etherscan.io/token/0x8bbfe65e31b348cd823c62e02ad8c19a84dd0dab) — source & docs: [mossland/MossCoin-ERC20-2025](https://github.com/mossland/MossCoin-ERC20-2025)
- Supported migration path: **Luniverse MOC → 2025 ERC-20**. This legacy 2018 ERC-20 is **not** part of the migration path, and the Wrapped MOC (WMOC) swap route is inactive.

> ⚠️ **Anti-phishing:** only use the current 2025 mainnet address above, confirmed via official Mossland channels. Do not deposit to, or swap from, the legacy contracts below.

---

## Legacy contracts (reference only — do not use)
- [Legacy 2018 ERC-20 (this repo)](https://etherscan.io/token/0x865ec58b06bf6305b886793aa20a2da31d034e68)
- [Luniverse MOC (LMT)](https://scan.luniverse.io/tokens/0x878120A5C9828759A250156c66D629219F07C5c6)

---

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
git clone --recursive git@github.com:mossland/MossCoin.git
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

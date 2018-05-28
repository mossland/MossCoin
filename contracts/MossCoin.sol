pragma solidity ^0.4.21;

import "./ownership/Ownable.sol";
import "./token/BurnableToken.sol";
import "./token/UpgradableToken.sol";
import "./token/StoppableToken.sol";

contract MossCoin is StoppableToken, UpgradableToken, BurnableToken {
    string public constant name = "Moss Coin";
    string public constant symbol = "MOC";
    uint8 public constant decimals = 18;

    function MossCoin(uint256 _amount) public
        Ownable()
    {
        totalSupply = _amount * 1 ether;
        balances[owner] = totalSupply;
    }
}
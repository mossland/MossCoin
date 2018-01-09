pragma solidity ^0.4.18;

import '../ownership/Ownable.sol';
import './BasicToken.sol';

contract BurnableToken is BasicToken, Ownable {
    event Burn(uint256 value);

    function burn(uint256 _value) onlyOwner public {
        require(_value <= balances[owner]);

        balances[owner] = balances[owner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        Burn(_value);
    }
}
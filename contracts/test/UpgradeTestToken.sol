pragma solidity ^0.4.21;

import "../token/StandardToken.sol";
import "../token/UpgradableToken.sol";
import "../math/SafeMath.sol";

contract UpgradeTestToken is StandardToken, UpgradeAgent {
    using SafeMath for uint256;
    UpgradableToken public oldToken;
    uint256 public oldSupply;

    function UpgradeTestToken(UpgradableToken _oldToken) public {
        require(address(_oldToken) != address(0));
        require(_oldToken.totalSupply() != 0);

        oldToken = _oldToken;
    }

    function upgradeFrom(address _from, uint256 _value) public {
        require(msg.sender == address(oldToken));
        totalSupply = totalSupply.add(_value);
        balances[_from] = balances[_from].add(_value);
    }

    function() public payable {
        assert(false);
    }
}
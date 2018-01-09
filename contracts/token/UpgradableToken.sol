pragma solidity ^0.4.18;

import '../ownership/Ownable.sol';
import '../math/SafeMath.sol';
import './StandardToken.sol';

contract UpgradeAgent {
    function upgradeFrom(address _from, uint256 _value) public;
}

contract UpgradableToken is StandardToken, Ownable {
    using SafeMath for uint256;

    address public upgradeAgent;
    uint256 public totalUpgraded;

    event Upgrade(address indexed _from, address indexed _to, uint256 _value);

    function upgrade(uint256 _value) external {
        assert(upgradeAgent != address(0));
        require(_value != 0);
        require(_value <= balances[msg.sender]);

        balances[msg.sender] -= _value;
        totalSupply -= _value;
        totalUpgraded += _value;
        UpgradeAgent(upgradeAgent).upgradeFrom(msg.sender, _value);
        Upgrade(msg.sender, upgradeAgent, _value);
    }

    function setUpgradeAgent(address _agent) external onlyOwner {
        require(_agent != address(0));
        assert(upgradeAgent == address(0));
        
        upgradeAgent = _agent;
    }
}
pragma solidity ^0.4.18;
import '../math/SafeMath.sol';
import '../ownership/Ownable.sol';
import './StandardToken.sol';

contract CrowdsaleToken is StandardToken, Ownable {
    using SafeMath for uint256;
    mapping (address => bool) public crowdsales;

    event Sale(address to, uint256 value);
    event SetCrowdsale(address addr, bool state);

    function setCrowdsale(address _addr, bool _state) onlyOwner public {
        crowdsales[_addr] = _state;
        SetCrowdsale(_addr, _state);
    }

    modifier onlyCrowdsale() {
        require(crowdsales[msg.sender]);
        _;
    }

    function sale(address _to, uint256 _value) public onlyCrowdsale returns (bool) {
        require(_to != address(0));
        require(_value <= balances[owner]);

        balances[owner] = balances[owner].sub(_value);
        balances[_to] = balances[_to].add(_value);
        Sale(_to, _value);
        return true;
    }
}
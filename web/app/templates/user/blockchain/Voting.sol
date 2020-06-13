pragma solidity ^0.6.4;
// We have to specify what version of compiler this code will compile with

contract Voting {
  /* mapping field below is equivalent to an associative array or hash.
  The key of the mapping is candidate name stored as type bytes32 and value is
  an unsigned integer to store the vote count
  */
  bytes32 public hash_md5;

  /* This is the constructor which will be called once when you
  deploy the contract to the blockchain. 
  */
  constructor() public {
    hash_md5 = 0;
  }

  // This function returns the total votes a candidate has received so far

  function getHash() public view returns (bytes32) {
    return hash_md5;
  }

  // This function increments the vote count for the specified candidate. This
  // is equivalent to casting a vote

  function changeHash(bytes32 new_hash) public {
    hash_md5 = new_hash;
  }

  function checkHash(bytes32 new_hash) public view returns (uint8){
    if (hash_md5 == new_hash)
      return 1;
    return 0;
  }
}
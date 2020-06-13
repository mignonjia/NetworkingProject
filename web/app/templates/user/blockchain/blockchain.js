web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"))
var account;
web3.eth.getAccounts().then((f) => {
 account = f[0];
})

abi = JSON.parse(fs.readFileSync('Voting_sol_Voting.abi').toString());

contract = new web3.eth.Contract(abi);
contract.options.address = "0xC3a95139775026125596b76BF262E003cfc930B2";
// update this contract address with your contract address

function changeHash() {
 hash_md5 = 0;

 contract.methods.changeHash(web3.utils.asciiToHex(hash_md5)).send({from: '0x4690f82fE53C9144c420eb83441f2dC7E0dbF7b0'}).then((f) => {
  let div_id = "hash_val";
  contract.methods.getHash().call().then((f) => {
   $("#" + div_id).html(f);
  })
 })
}

$(document).ready(function() {
    contract.methods.getHash().call().then((f) => {
        $("#"+"hash_val").html(f);
    })
});


web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"))
var account;
web3.eth.getAccounts().then((f) => {
 account = f[0];
})

//abi = JSON.parse('[{"constant":true,"inputs":[{"name":"candidate","type":"bytes32"}],"name":"validCandidate","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"candidate","type":"bytes32"}],"name":"getHash","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"bytes32"}],"name":"votesReceived","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"hash_md5","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"candidate","type":"bytes32"}],"name":"voteForCandidate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"candidateNames","type":"bytes32[]"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
//abi = JSON.parse('[{"constant":true,"inputs":[],"name":"getHash","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"bytes32"}],"name":"hash_md5","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]');
abi = JSON.parse('[{"constant":true,"inputs":[{"name":"new_hash","type":"bytes32"}],"name":"checkHash","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"new_hash","type":"bytes32"}],"name":"changeHash","outputs":[],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getHash","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"bytes32"}],"name":"hash_md5","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]');

contract = new web3.eth.Contract(abi);
contract.options.address = "0x88122c0531F5feF0eDe322B3a2880061f1e9e173";
// update this contract address with your contract address



function changeHash(new_hash) {
  new_hash_val = $("#new_hash").val();
  contract.methods.changeHash(web3.utils.asciiToHex(new_hash_val)).send({from: account}).then((f) => {
    contract.methods.getHash().call().then((f) => {
     $("#hash_val").html(f);
    })
   })
}

function checkHash(new_hash) {
  new_hash_val = $("#new_hash2").val();
  contract.methods.checkHash(web3.utils.asciiToHex(new_hash_val)).send({from: account}).then((f) => {
    $("#check_hash").html(f);
   })
}

$(document).ready(function() {
    alert("成功执行ready");
 contract.methods.getHash().call().then((f) => {
  $("#hash_val").html(f);
})
});
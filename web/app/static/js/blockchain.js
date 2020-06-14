
web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"))
var account;
web3.eth.getAccounts().then((f) => {
 account = f[0];
})

//abi = JSON.parse('[{"constant":true,"inputs":[{"name":"candidate","type":"bytes32"}],"name":"validCandidate","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"candidate","type":"bytes32"}],"name":"getHash","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"bytes32"}],"name":"votesReceived","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"hash_md5","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"candidate","type":"bytes32"}],"name":"voteForCandidate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"candidateNames","type":"bytes32[]"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
abi = JSON.parse('[{"constant":true,"inputs":[],"name":"getHash","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"bytes32"}],"name":"hash_md5","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]');


contract = new web3.eth.Contract(abi);
// contract.options.address = "0xDCCdd416eBb79b16ee5EA1520215a9ec5A98c978";
contract.options.address = "0x55feCc64C89E0C9Dc2DFCD33Ca391199dcF76968";
// update this contract address with your contract address

function getHash() {}

$(document).ready(function() {
    alert("成功执行");
    document.getElementById("hash_val").innerHTML = "test";
    
    contract.methods.getHash().call().then((f) => {
    $("#hash_val").html(f);
    document.getElementById("hash_val").innerHTML = f;
})
});

window.onload=function() {
    alert("成功执行test2");
    document.getElementById("hash_val").innerHTML = "test onload2";
}


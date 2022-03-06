require("dotenv").config();
const Web3 = require("web3");

// ADDRESS, KEY and URL are examples.
const CONTRACT_ADDRESS = "0xb25D8ce278A5aa2f71528d4e7b5daE9C1288DD7e";
const PUBLIC_KEY = "0xb25D8ce278A5aa2f71528d4e7b5daE9C1288DD7e";
const PROVIDER_URL =
    "https://eth-ropsten.alchemyapi.io/v2/" + process.env.ALCHEMY_API_KEY;

async function viewNFT() {
    const web3 = new Web3(PROVIDER_URL);
    const contract = require("../artifacts/contracts/Token.sol/Token.json");
    // console.log("contract", contract);

    const nftContract = new web3.eth.Contract(
        contract.abi, CONTRACT_ADDRESS
    );
    console.log("nftContract", nftContract);

    nftContract.methods.balanceOf(PUBLIC_KEY).call().then(console.log);
    // nftContract.methods.balanceOf(PUBLIC_KEY).call().then((e) => {
    //     console.log("e", e);
    // });
}

viewNFT();

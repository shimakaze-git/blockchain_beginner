const { ethers } = require("ethers");

const initialize = () => {
    let accounts;

    const onboardButton = document.getElementById('connectButton');
    const retrieveButton = document.getElementById('retrieveButton');
    const storeButton = document.getElementById('storeButton');
    const messageStatus = document.getElementById('messageStatus');
    const inputMessage = document.getElementById('inputMessage');
    const accountsDiv = document.getElementById('accounts');

    let myContract;
    //enter deployed contract abi
    const ContractAbi = [
        {},
        {}
    ];

    const ContractAddress = "0x***";
    const isMetaMaskConnected = () => accounts && accounts.length > 0

    const isMetaMaskInstalled = () => {
        const { ethereum } = window;

        console.log("ethereum.isMetaMask", ethereum.isMetaMask)
        return Boolean(
            ethereum && ethereum.isMetaMask
        );
    };

    // onClickConnect
    const onClickConnect = async () => {
        try {
            const newAccounts = await ethereum.request({
                method: 'eth_requestAccounts',
            })
            accounts = newAccounts;
            console.log("accounts", accounts)

            // accountsDiv.innerHTML = accounts;
            // if (isMetaMaskConnected()) {
            //     retrieveButton.disabled = false;
            //     retrieveButton.onclick = onClickRetrieve;
            //     storeButton.disabled = false;
            //     storeButton.onclick = onClickStore;
            //     const provider = new ethers.providers.Web3Provider(window.ethereum);
            //     const signer = provider.getSigner(0);
            //     myContract = new ethers.Contract(ContractAddress, ContractAbi, signer);
            // }
        } catch (error) {
            console.error(error);
        }
    }

    // onClickRetrieve

    // onClickStore

    const MetaMaskClientCheck = () => {
        console.log("MetaMaskClientCheck")

        if (!isMetaMaskInstalled()) {
            onboardButton.innerText = 'Please install MetaMask';
        } else {
            onboardButton.innerText = 'Connect';
            onboardButton.onclick = onClickConnect;
            onboardButton.disabled = false;
        }
    };
    MetaMaskClientCheck();
};
window.addEventListener('DOMContentLoaded', initialize)
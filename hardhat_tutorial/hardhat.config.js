require("dotenv").config();
require("@nomiclabs/hardhat-waffle");

// alchemyのAPIキー
// const ALCHEMY_API_KEY = "";

// Repstenネットワークを設定しているMetamaskアカウントの秘密鍵
// const ROPSTEN_PRIVATE_KEY = "";

/**
 * @type import('hardhat/config').HardhatUserConfig
 */
module.exports = {
  solidity: "0.7.3",

  // 以下を追加
  networks: {
    ropsten: {
      url: "https://eth-ropsten.alchemyapi.io/v2/" + process.env.ALCHEMY_API_KEY,
      // url: `https://eth-ropsten.alchemyapi.io/v2/${ALCHEMY_API_KEY}`,
      accounts: [
        process.env.ROPSTEN_PRIVATE_KEY
      ]
      // accounts: [
      //   `${ROPSTEN_PRIVATE_KEY}`
      // ]
    }
  }
};

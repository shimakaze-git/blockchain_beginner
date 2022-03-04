// const Migrations = artifacts.require("Migrations");
const Message = artifacts.require("Message");

module.exports = function (deployer) {
  // deployer.deploy(Migrations);
  deployer.deploy(Message);
};

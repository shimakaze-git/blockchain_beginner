const bitcore = require('bitcore-lib');
const network = 'testnet';

// 秘密鍵を作成
const privateKey = new bitcore.PrivateKey(network);

// ビットコインアドレスを作成
const address = privateKey.toAddress();

console.log(privateKey.toString());
console.log(address.toString());

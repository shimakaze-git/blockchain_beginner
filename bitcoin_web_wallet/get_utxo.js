const explorers = require('bitcore-explorers');

const network = 'testnet'
const address = 'mjNYVntJJqLGvMfhvk8kiW4ZsvubRD9b5h';
const insight = new explorers.Insight(network);

insight.getUnspentUtxos(address, (err, utxos) => {
    console.log('address : ', address);
    console.log("utxos : ", utxos);

    if (err) {
        console.log('UTXO processing error')
    } else {
        let balance = utxos.map((v) => {
            return {
                txid: v.txid,
                vout: v.outputIndex,
                satoshi: v.satoshis,
                btc: v.satoshis * 1e-8,
            }
        })
        console.log(JSON.stringify(balance));
    }
});
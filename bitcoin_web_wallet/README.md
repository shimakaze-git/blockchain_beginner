## 秘密鍵とアドレスの作成

bitcore-libを使ってビットコインアドレスを作成。
ビットコインアドレスは秘密鍵から公開鍵、公開鍵からビットコインアドレスを作成する。
bitcore-libを使うと秘密鍵の生成からアドレスの作成までを簡単に行うことができる。
今回はテストネット（価値のない開発用のビットコインを使ったネットワーク）で開発を行い、ネットワークには'testnet'に指定。

```javascript
const bitcore = require('bitcore-lib');
const network = 'testnet';

// 秘密鍵を作成
const privateKey = new bitcore.PrivateKey(network);

// ビットコインアドレスを作成
const address = privateKey.toAddress();

console.log(privateKey.toString());
console.log(address.toString());
```

実行結果
```
8a9293084ae896edf95566836948b568d1f8cdc170990178357ed425218a0494
mjNYVntJJqLGvMfhvk8kiW4ZsvubRD9b5h
```

## 秘密鍵に紐づく残高(UTXO)の確認

ビットコインでは分散型台帳を採用しており、銀行のように顧客IDなどに直接残高を紐づけて記録するシステムでは無い。

ビットコインは保有する秘密鍵に紐づいた未使用トランザクション(UTXO)をネットワークから調べ、そのUTXOの総数をカウントする事で保有する残高を知ることができる。

残高を確認する為に、先ほど作成しましたアドレスにテストネットのコインを送金してみます。
テストネットのコインは[faucet](https://coinfaucet.eu/en/btc-testnet/)で無料で配布されています。
作成したアドレスを「Your testnet3 adress」に指定し「Get bitcoins!」を押すとアドレス宛に少量のテストネットコインが届きます。

```javascript
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
```

## 送金処理の作成

faucetで手に入れたテストネットのコインを送金してみる。

送金するためにはトランザクションを作成する必要があり、トランザクションには手数料, UTXO, 送金額, 送金アドレス, お釣り受け取りアドレス, 秘密鍵による署名を含める必要がある。
これらの情報を含んだトランザクションを作成し、ビットコインネットワークにブロードキャストする。

```javascript
const bitcore = require('bitcore-lib')
const explorers = require('bitcore-explorers')

const network = 'testnet'
const privatekey = '8a9293084ae896edf95566836948b568d1f8cdc170990178357ed425218a0494';
const privateKey = new bitcore.PrivateKey(privatekey);
const sendAddress = 'mq8aTnusvudJBr2A4iNmCpQkWS8SQuALGD';
// const changeAddress = 'msQXdd2gDGWSYaDF32TEWb3Yji7mbk3VCJ';
const changeAddress = 'mjNYVntJJqLGvMfhvk8kiW4ZsvubRD9b5h';
const sendAmout = Math.floor(parseFloat("0.0001") * 100000000);
const fee = parseFloat(1000);
const insight = new explorers.Insight(network);
const Transaction = bitcore.Transaction;


insight.getUnspentUtxos(changeAddress, (err, utxos) => {
    if (err) {
        console.log('Bitcoin network connection error');
    } else {

        const transaction = new Transaction()
            .fee(fee)
            .from(utxos)
            .to(sendAddress, sendAmout)
            .change(changeAddress)
            .sign(privateKey)

        insight.broadcast(transaction, (err, returnedTxId) => {
            if (err) {
                console.log(err);
            } else {
                console.log('returnedTxId : ', returnedTxId);
            }
        });
    }
});
```

実行結果
```
returnedTxId :  31e9bc135c77ac6fe0ec969a7f175ca899aa4a3b9d6dc3d3a01eba77cf7294e0
```

画面に表示されたトランザクションIDを[blockcypher](https://live.blockcypher.com/btc-testnet/)で、実際にテストコインの送金が本当に成功しているのか確認。
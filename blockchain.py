import hashlib
import json
from time import time

from uuid import uuid4

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        
        # 一番初めに作成されるブロック
        self.new_block(previous_hash=1, proof=100)
        
    def new_block(self, proof, previous_hash=None):
        """
        ブロックチェーンに新しいブロックを作成する
        :param proof: <int> Proof of Workアルゴリズムによって与えられた証明
        :param previous_hash: (Optional) <str> 前のブロックのハッシュ値
        :return: <dict> 新しいブロック
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # 現在のトランザクションのリストをリセット
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        新しいトランザクションを作成し、次のマイニングされたブロックに入る。
        :param sender: <str> 送信者アドレス
        :param recipient: <str> 受取人のアドレス
        :param amount: <int> 数(金額)
        :return: <int> このトランザクションのブロックのインデックス
        """
        
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        # チェーン内の最後のブロックを返す
        
        return self.chain[-1]
        
    @staticmethod
    def hash(block):
        """
        ブロックのSHA-256ハッシュ値を作成
        :param block: <dict> ブロック
        :return: <str>
        """
        
        # 辞書が順序付けされていることを確認する必要があります。
        # 又は一貫性のないハッシュを持ちたい
        
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
        
    def proof_of_work(self, last_proof):
        """
        簡単なProof of Work アルゴリズム
         - ハッシュ（pp '）に先行する4つのゼロが含まれるような数p'を見つけます。ここではpは前のp'です。
         - pは前の証明であり、p'は新しい証明です
        :param last_proof: <int>
        :return: <int>
        """

        proof = 0
        # while self.valid_proof(last_proof, proof) is False:
        #     proof += 1

        return proof
        
    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """
        
        # guess = f'{last_proof}{proof}'.encode()
        # guess_hash = hashlib.sha256(guess).hexdigest()
        
        # return guess_hash[:4] == "0000"
        pass
        
        
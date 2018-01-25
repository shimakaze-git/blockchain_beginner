import hashlib
import json
from textwrap import dedent

from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()
        
        # 一番初めに作成されるブロック
        self.new_block(previous_hash=1, proof=100)
        
    def register_node(self, address):
        """
        ノードのリストに新しいノードを追加する
        :param address: <str> ノードのアドレス. Eg. 'http://192.168.0.5:5000'
        :return: None
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    def valid_chain(self, chain):
        """
        特定のブロックチェーンが有効かどうかを判断
        :param chain: <list> ブロックチェーン
        :return: <bool> 有効であれば真、そうでなければ偽
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            
            # ブロックのハッシュが正しいことを確認
            if block['previous_hash'] != self.hash(last_block):
                return False

            # プルーフオブワークが正しいことを確認する
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True
        
    def resolve_conflicts(self):
        """
        これはコンセンサスアルゴリズムであり、チェーンを
        ネットワーク内で最長のものに置き換えることによって競合を解決します。
        :return: <bool> チェーンが交換された場合はTrue、そうでない場合はFalse
        """

        neighbours = self.nodes
        new_chain = None

        # 私たちは私たちより長い鎖を探している
        max_length = len(self.chain)

        # ネットワーク内のすべてのノードからチェーンを取得し、検証する
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # 長く、チェーンが有効であることを確認
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # 私たちのチェーンよりも新しい、有効なチェーンが発見されたら、チェーンを交換
        if new_chain:
            self.chain = new_chain
            return True

        return False
        
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
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof
        
    @staticmethod
    def valid_proof(last_proof, proof):
        """
        証明を検証する：ハッシュ（last_proof、proof）に4つの先頭0が含まれているか？
        :param last_proof: <int> 前の証明
        :param proof: <int> 現在の証明
        :return: <bool> 正しい場合はTrue、そうでない場合はFalse
        """
        
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        
        return guess_hash[:4] == "0000"
        
        
        

# ノードのインスタンス化
app = Flask(__name__)

# このノードためのグローバルユニーク(一意)のアドレスを生成する
node_identifier = str(uuid4()).replace('-', '')

# ブロックチェーンをインスタンス化
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    # 新しいブロックをマイニングする
    
    # 次の証明を得るためにプルーフオブワークアルゴリズムを実行
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    
    # 証拠を見つけるための報酬を受け取らなければならない
    # 送信者は、このノードが新しいコインをマイニングしたことを示す「0」である
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )
    
    # 新しいブロックをチェーンに追加して偽造
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200
    
  
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    # 新しいトランザクションを加えていく　
    
    # リクエストされたjsonデーターを受け取る
    values = request.get_json()

    # POSTされたデータに必要なフィールドがあることを確認
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # 新しいトランザクションを作成
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201
    
    
@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200
    
@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201
    
@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201
    
@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

if __name__ == '__main__':
    from argparse import ArgumentParser
    
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
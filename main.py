import hashlib
import json
import time
import requests
from flask import Flask, jsonify, request
from urllib.parse import urlparse

def hashGenerator(data):
    result = hashlib.sha256(data.encode())
    return result.hexdigest()


class Block:
    def __init__(self, index, timestamp, data, hash, prev_hash):
        self.index= index
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
        self.prev_hash = prev_hash

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        hashLast = hashGenerator('last_gen')
        hashFirst = hashGenerator('first_gen')

        genesis = Block(0, time.time(), 'gen_data', hashFirst, hashLast)
        self.chain = [genesis]

        self.nodes = set()

    def add_block(self, data):
        prev_hash = self.chain[-1].hash
        hash = hashGenerator(data+prev_hash)
        block = Block(self.chain[-1].index + 1, time.time(), data, hash, prev_hash)
        self.chain.append(block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.prev_hash != previous_block.hash:
                return False
        return True

    def register_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def consensus(self):
        neighbors = self.nodes
        new_chain = None
        max_length = len(self.chain)

        for node in neighbors:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid():
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False

app = Flask(__name__)

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    # Implement node registration logic here
    return "Nodes registered successfully", 201

@app.route('/nodes', methods=['GET'])
def get_nodes():
    # Implement logic to get the list of nodes
    nodes = [...]  # Replace [...] with actual list of nodes
    return jsonify(nodes), 200

if __name__ == '__main__':
    blch = Blockchain()
    blch.add_block('A')
    blch.add_block('B')
    blch.add_block('C')
    for block in blch.chain:
        print(block.__dict__)
    app.run(debug=True)


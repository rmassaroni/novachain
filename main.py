import hashlib
import json
import time

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


blch = Blockchain()
blch.add_block('A')
blch.add_block('B')
blch.add_block('C')

for block in blch.chain:
    print(block.__dict__)

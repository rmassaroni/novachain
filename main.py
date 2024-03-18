import hashlib

def hashGenerator(data):
    result = hashlib.sha256(data.encode())
    return result.hexdigest()


class Block:
    def __init__(self, data, hash, prev_hash):
        self.data = data
        self.hash = hash
        self.prev_hash = prev_hash


class MyBlockchain:
    def __init__(self):
        hashLast = hashGenerator('last_gen')
        hashFirst = hashGenerator('first_gen')

        genesis = Block('gen_data', hashFirst, hashLast)
        self.chain = [genesis]

    def add_block(self, data):
        prev_hash = self.chain[-1].hash
        hash = hashGenerator(data+prev_hash)
        block = Block(data,hash,prev_hash)
        self.chain.append(block)


blch = MyBlockchain()
blch.add_block('A')
blch.add_block('B')
blch.add_block('C')

for block in blch.chain:
    print(block.__dict__)

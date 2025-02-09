decentralized_network.py
import hashlib
import json
from urllib.parse import urlparse
import requests
from collective_intelligence_engine import CollectiveIntelligenceEngine
class Block:
    def __init__(self, index, previous_hash, timestamp, data):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = self.calculate_hash()
    def calculate_hash(self):
        data_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(data_string.encode()).hexdigest()
class DecentralizedNetwork:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.nodes = set()
        self.engine = CollectiveIntelligenceEngine()
    def create_genesis_block(self):
        return Block(0, "0", 1643723906, "Genesis Block")
    def get_latest_block(self):
        return self.chain[-1]
    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    def replace_chain(self):
        network = self
        longest_chain = None
        max_length = len(network.chain)
        for node in network.nodes:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length:
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            network.chain = longest_chain
            return True
        return False

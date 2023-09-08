import hashlib
import json
from time import time

# Define the Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = []  # List to store blocks
        self.current_transactions = []  # List to store pending transactions

        # Create the genesis block
        self.new_block(previous_hash="1", proof=100)

    # Create a new block
    def new_block(self, proof, previous_hash=None):
        """
        Create a new block in the blockchain

        :param proof: The proof of work
        :param previous_hash: Hash of the previous block
        :return: New block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    # Hash a block using SHA-256
    @staticmethod
    def hash(block):
        """
        Create a SHA-256 hash of a block

        :param block: Block
        :return: Hash
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    # Create a new transaction
    def new_transaction(self, sender, recipient, amount):
        """
        Create a new transaction to go into the next mined block

        :param sender: Address of the sender
        :param recipient: Address of the recipient
        :param amount: Amount
        :return: Index of the block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    # Simulate block mining
    def mine_block(self, miner_address):
        # In a real cryptocurrency, mining would involve solving a complex proof-of-work puzzle.
        # For simplicity, we'll just add the pending transactions to a new block.
        proof = 12345  # Proof of work for mining
        previous_hash = self.hash(self.chain[-1])
        
        # Reward the miner
        miner_reward = 1
        self.new_transaction(sender="0", recipient=miner_address, amount=miner_reward)
        
        block = self.new_block(proof, previous_hash)
        return block

    # Get the last block in the chain
    @property
    def last_block(self):
        return self.chain[-1]


# Define the Wallet class
class Wallet:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.balance = 0

    # Generate a public-private key pair
    def generate_key_pair(self):
        """
        Generate a new public-private key pair for the wallet.
        For simplicity, we'll use a single key pair for the wallet.
        In a real-world scenario, you'd manage a key pair securely.
        """
        # Generate a key pair (simplified for demonstration)
        self.private_key = "my_private_key"  # In practice, use a secure key generation method
        self.public_key = "my_public_key"    # In practice, derived from the private key

    # Send funds from the wallet
    def send_funds(self, recipient, amount):
        if amount <= 0:
            return "Invalid amount"

        if self.balance < amount:
            return "Insufficient funds"

        sender = self.public_key  # Define the sender
        index = self.blockchain.new_transaction(sender, recipient, amount)  # Pass sender, recipient, and amount separately

        # Create a new transaction
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        }

        # Sign the transaction with the wallet's private key (simplified for demonstration)
        transaction['signature'] = self.sign_transaction(transaction)

        # Update the wallet's balance
        self.balance -= amount

        return f"Transaction added to block {index} successfully."

    # Simulate receiving funds
    def receive_funds(self, amount):
        if amount <= 0:
            return "Invalid amount"

        # Simulate receiving funds
        self.balance += amount
        return "Funds received"

    # Sign a transaction using the wallet's private key
    def sign_transaction(self, transaction):
        """
        Sign a transaction using the wallet's private key.
        In a real-world scenario, use a secure signing method.
        """
        return "signature_here"  # In practice, use cryptographic signing

# Create a new blockchain
blockchain = Blockchain()

# Create a wallet and generate key pair for Jason
jason_wallet = Wallet(blockchain)
jason_wallet.generate_key_pair()

# Receive initial funds for Jason
jason_wallet.receive_funds(1000)

# Mine a block (simulated mining)
blockchain.mine_block(jason_wallet.public_key)

# Send funds to Bob
transaction_result = jason_wallet.send_funds("Bob's public key", 200)
print(transaction_result)

# Mine another block (simulated mining)
blockchain.mine_block(jason_wallet.public_key)

# Check Jason's balance after the transactions
print(f'Jason balance: {jason_wallet.balance}')

# Print the blockchain in a simplified format
print("Blockchain:")
for block in blockchain.chain:
    print(f"Block {block['index']}:")
    print("- Transactions:")
    
    for transaction in block['transactions']:
        if 'sender' in transaction:
            if transaction['sender'] == "0":
                print(f"  - Miner Reward: {transaction['amount']}")
            else:
                print(f"  - From: {transaction['sender']}")
                print(f"  - To: {transaction['recipient']}")
                print(f"  - Amount: {transaction['amount']}")
        else:
            print(f"  - Miner Reward: {transaction['miner_reward']}")
    
    print()

import hashlib
import json
import random
import time
from datetime import datetime

# Sample list of Ethereal wallet addresses
ethereal_wallets = [f"0xWallet{i}" for i in range(1, 6)]

# Initialize a dictionary to store wallet balances with a default balance of 0
wallet_balances = {wallet: 0 for wallet in ethereal_wallets}

# Initialize an empty list to store transactions
transactions = []

# Function to generate a random Ethereal transaction with user input for amount
def generate_ethereal_transaction(sender, receiver, eth_amount):
    return sender, receiver, eth_amount

# Create a new blockchain
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash="1", proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new block in the blockchain

        :param proof: The proof of work
        :param previous_hash: Hash of the previous block
        :return: New block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time.time(),  # Use time.time() to get the current timestamp
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    @staticmethod
    def hash(block):
        """
        Create a SHA-256 hash of a block

        :param block: Block
        :return: Hash
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

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

    @property
    def last_block(self):
        return self.chain[-1]

# Save Wallet Balances and Transactions to a JSON file
def save_data():
    data = {
        "wallet_balances": wallet_balances,
        "transactions": transactions
    }
    with open("blockchain_data.json", "w") as file:
        json.dump(data, file)

# Load Wallet Balances and Transactions from a JSON file
def load_data():
    try:
        with open("blockchain_data.json", "r") as file:
            data = json.load(file)
            return data.get("wallet_balances", {}), data.get("transactions", [])
    except FileNotFoundError:
        return {}, []

# Load data at the beginning of the program
wallet_balances, transactions = load_data()

# Create a blockchain
blockchain = Blockchain()

# Welcome message and user menu
print("Welcome to Ethereal Blockchain Simulator!")
while True:
    print("\nMenu:")
    print("1. Simulate Ethereal Transactions")
    print("2. Display Wallet Balances")
    print("3. Display Blockchain")
    print("4. Exit")

    choice = input("Enter your choice (1/2/3/4): ")

    if choice == "1":
        num_transactions = int(input("Enter the number of transactions you want to simulate: "))
        for _ in range(num_transactions):
            print("\nAvailable Wallets:")
            for i, wallet in enumerate(ethereal_wallets):
                print(f"{i + 1}. {wallet}")

            sender_index = int(input("Enter the sender's wallet number (1 to 5): ")) - 1
            receiver_index = int(input("Enter the receiver's wallet number (1 to 5, different from sender): ")) - 1

            if sender_index == receiver_index or not (0 <= sender_index < len(ethereal_wallets)) or not (0 <= receiver_index < len(ethereal_wallets)):
                print("Invalid input. Sender and receiver must be different and within the range.")
                continue

            eth_amount = round(float(input("Enter the ETH amount to send: ")), 2)
            sender = ethereal_wallets[sender_index]
            receiver = ethereal_wallets[receiver_index]

            print(f"Simulating Ethereal Transaction: {sender} -> {receiver}, Amount: {eth_amount} ETH")

            # Add the transaction to the list
            transactions.append((sender, receiver, eth_amount))

            # Update wallet balances
            wallet_balances[sender] -= eth_amount
            wallet_balances[receiver] += eth_amount

            # Add the transaction to the blockchain
            blockchain.new_transaction(sender, receiver, eth_amount)

            # Save the updated data to the JSON file
            save_data()

            # Add a 1-second delay
            time.sleep(1)

        print("Transactions simulated successfully!")

    elif choice == "2":
        # Display wallet balances
        print("\nWallet Balances:")
        for wallet, balance in wallet_balances.items():
            print(f"{wallet}: {balance} ETH")

    elif choice == "3":
        # Display the blockchain
        print("\nBlockchain:")
        for block in blockchain.chain:
            print(f"Block {block['index']}:")
            print(f"- Timestamp: {datetime.utcfromtimestamp(block['timestamp']).strftime('%Y-%m-%d %H:%M:%S')} UTC")
            print(f"- Previous Hash: {block['previous_hash']}")
            print(f"- Proof: {block['proof']}")
            print(f"- Transactions:")

            for transaction in block['transactions']:
                print(f"  - Sender: {transaction['sender']}")
                print(f"  - Receiver: {transaction['recipient']}")
                print(f"  - Amount: {transaction['amount']} ETH")

        

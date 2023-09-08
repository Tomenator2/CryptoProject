import random
import time

# Sample list of Ethereum wallet addresses
eth_wallets = ["0xWallet1", "0xWallet2", "0xWallet3", "0xWallet4", "0xWallet5"]

# Initialize an empty list to store transactions
transactions = []

# Function to generate a random Ethereum transaction
def generate_fake_eth_transaction():
    sender = random.choice(eth_wallets)
    receiver = random.choice(eth_wallets)
    while sender == receiver:
        receiver = random.choice(eth_wallets)
    eth_amount = round(random.uniform(0.01, 10), 2)  # Simulate ETH amounts
    return sender, receiver, eth_amount

# Simulate Ethereum transactions based on user input
num_transactions = int(input("Enter the number of transactions you want to simulate: "))
for _ in range(num_transactions):
    print("\nAvailable Wallets:")
    for i, wallet in enumerate(eth_wallets):
        print(f"{i+1}. {wallet}")
    
    sender_index = int(input("Enter the sender's wallet number (1 to 5): ")) - 1
    receiver_index = int(input("Enter the receiver's wallet number (1 to 5, different from sender): ")) - 1
    
    if sender_index == receiver_index or not (0 <= sender_index < len(eth_wallets)) or not (0 <= receiver_index < len(eth_wallets)):
        print("Invalid input. Sender and receiver must be different and within the range.")
        continue
    
    eth_amount = round(float(input("Enter the ETH amount to send: ")), 2)
    sender = eth_wallets[sender_index]
    receiver = eth_wallets[receiver_index]
    
    print(f"Simulating Ethereum Transaction: {sender} -> {receiver}, Amount: {eth_amount} ETH")
    
    # Add the transaction to the list
    transactions.append((sender, receiver, eth_amount))
    
    # Add a 1-second delay
    time.sleep(1)

# Display all transactions at the end
print("\nAll Transactions:")
for i, (sender, receiver, amount) in enumerate(transactions, start=1):
    print(f"{i}. Sender: {sender}, Receiver: {receiver}, Amount: {amount} ETH")

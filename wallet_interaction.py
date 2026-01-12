import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from web3 import Web3
from eth_account import Account
import datetime

class EthereumWalletGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ethereum Wallet Demo")
        self.root.geometry("900x700")
        
        self.public_rpcs = [
            "https://rpc.sepolia.org",
            "https://rpc2.sepolia.org", 
            "https://eth-sepolia.g.alchemy.com/v2/demo",
            "https://11155111.rpc.thirdweb.com"
        ]
        
        self.w3 = None
        self.account_address = None
        self.simulated_balance = 0.0
        self.setup_gui()
        self.connect_to_network()
    
    def connect_to_network(self):
        for rpc_url in self.public_rpcs:
            try:
                self.w3 = Web3(Web3.HTTPProvider(rpc_url))
                if self.w3.is_connected():
                    self.network_label.config(text="✅ Connected: Sepolia")
                    self.log_message(f"✅ Connected!")
                    return True
            except:
                continue
    
    def setup_gui(self):
        status_frame = ttk.LabelFrame(self.root, text="Network", padding="10")
        status_frame.pack(fill="x", padx=10, pady=5)
        self.network_label = ttk.Label(status_frame, text="Connecting...")
        self.network_label.pack()
        
        # FIXED INPUT SECTION
        input_frame = ttk.LabelFrame(self.root, text="Wallet Address", padding="10")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text="Address:").grid(row=0, column=0, sticky="w", padx=(0,5))
        self.address_entry = ttk.Entry(input_frame, width=65)
        self.address_entry.grid(row=0, column=1, padx=5)
        # ✅ CORRECT TEST ADDRESS
        self.address_entry.insert(0, "0x742d35Cc6634C0532925a3b8D7c9fa368F067E6b")
        
        ttk.Button(input_frame, text="📱 Load Address", 
                  command=self.load_address).grid(row=0, column=2, padx=5)
        
        ttk.Button(input_frame, text="🆕 New Wallet", 
                  command=self.generate_demo_wallet).grid(row=1, column=1, pady=5)
        
        # Wallet Info
        wallet_frame = ttk.LabelFrame(self.root, text="Wallet Info", padding="10")
        wallet_frame.pack(fill="x", padx=10, pady=5)
        
        self.address_label = ttk.Label(wallet_frame, text="Address: Not loaded")
        self.address_label.pack(anchor="w")
        self.balance_label = ttk.Label(wallet_frame, text="Balance: 0 ETH")
        self.balance_label.pack(anchor="w")
        
        # Balance Controls - WORKING!
        balance_frame = ttk.LabelFrame(self.root, text="Balance Demo", padding="10")
        balance_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Button(balance_frame, text="💰 Check Real", 
                  command=self.check_real_balance).pack(side="left", padx=5)
        ttk.Button(balance_frame, text="➕ Add 0.1", 
                  command=lambda: self.change_balance(0.1)).pack(side="left", padx=5)
        ttk.Button(balance_frame, text="➖ Remove 0.1", 
                  command=lambda: self.change_balance(-0.1)).pack(side="left", padx=5)
        ttk.Button(balance_frame, text="🔄 Reset", 
                  command=self.reset_balance).pack(side="left", padx=5)
        
        # Transaction Demo
        tx_frame = ttk.LabelFrame(self.root, text="Send Demo", padding="10")
        tx_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(tx_frame, text="To:").grid(row=0, column=0, sticky="w")
        self.to_entry = ttk.Entry(tx_frame, width=50)
        self.to_entry.grid(row=0, column=1, padx=5)
        self.to_entry.insert(0, "0x742d35Cc6634C0532925a3b8D7c9fa368F067E6b")
        
        ttk.Label(tx_frame, text="ETH:").grid(row=1, column=0, sticky="w")
        self.amount_entry = ttk.Entry(tx_frame, width=10)
        self.amount_entry.grid(row=1, column=1, sticky="w", padx=5)
        self.amount_entry.insert(0, "0.01")
        
        ttk.Button(tx_frame, text="📤 Send Demo", 
                  command=self.demo_send).grid(row=2, column=1, pady=5)
        
        # Console
        output_frame = ttk.LabelFrame(self.root, text="Console", padding="10")
        output_frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.output_text = scrolledtext.ScrolledText(output_frame, height=10)
        self.output_text.pack(fill="both", expand=True)
    
    # ✅ FIXED VALIDATION
    def load_address(self):
        address = self.address_entry.get().strip()
        
        # Simple length + 0x check
        if not address.startswith('0x'):
            messagebox.showerror("Error", "Address must start with 0x")
            return
        if len(address) != 42:  # 0x + 40 chars
            messagebox.showerror("Error", "Address must be 42 characters (0x + 40)")
            return
        
        self.account_address = address
        self.address_label.config(text=f"✅ {address}")
        self.log_message(f"✅ LOADED: {address}")
        self.check_real_balance()
    
    def generate_demo_wallet(self):
        demo_account = Account.create()
        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, demo_account.address)
        self.log_message(f"🆕 New: {demo_account.address}")
    
    def check_real_balance(self):
        if not self.account_address or not self.w3:
            self.log_message("⚠️ Load address first")
            return
        
        try:
            balance_wei = self.w3.eth.get_balance(self.account_address)
            real_balance = self.w3.from_wei(balance_wei, 'ether')
            self.log_message(f"🌐 REAL: {real_balance:.6f} ETH")
        except Exception as e:
            self.log_message(f"ℹ️ Real balance unavailable")
    
    def change_balance(self, amount):
        if not self.account_address:
            self.log_message("⚠️ Load address first")
            return
        
        self.simulated_balance += amount
        self.balance_label.config(text=f"Demo: {self.simulated_balance:.4f} ETH")
        self.log_message(f"💰 {'+' if amount > 0 else ''}{amount:.3f} ETH | Total: {self.simulated_balance:.4f}")
    
    def reset_balance(self):
        self.simulated_balance = 0.0
        self.balance_label.config(text="Demo: 0.0000 ETH")
        self.log_message("🔄 Reset to 0")
    
    def demo_send(self):
        if not self.account_address:
            self.log_message("⚠️ Load address first")
            return
        
        try:
            amount = float(self.amount_entry.get() or 0)
            self.simulated_balance -= amount
            self.balance_label.config(text=f"Demo: {self.simulated_balance:.4f} ETH")
            self.log_message(f"📤 SENT {amount} ETH | New: {self.simulated_balance:.4f} ETH")
        except:
            self.log_message("❌ Invalid amount")
    
    def log_message(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.output_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.output_text.see(tk.END)

def main():
    root = tk.Tk()
    app = EthereumWalletGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

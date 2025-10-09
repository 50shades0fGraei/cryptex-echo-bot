from trade_sell import execute_sell
from royalty_logger import read_log

def menu():
    print("\nGraeiTrade Console")
    print("1. Execute Trade")
    print("2. View Royalty Log")
    print("3. Exit")

def run():
    while True:
        menu()
        choice = input("Select: ")
        if choice == "1":
            asset = input("Asset name: ")
            price = float(input("Asset price: "))
            qty = int(input("Quantity: "))
            trade_id = input("Trade ID: ")
            from trade_sell import Trade
            trade = Trade(trade_id, asset, price, qty)
            execute_sell(trade)
        elif choice == "2":
            log = read_log()
            for entry in log:
                print(entry)
        elif choice == "3":
            break

if __name__ == "__main__":
    run()

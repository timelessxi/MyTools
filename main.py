from colorama import init, Fore, Style

init(autoreset=True)

from delivery_box import deliver
from auction_house import update_auction_house, buy_all_items, buy_random_items
from inventory_manager import InventoryManager


class GameToolbox:
    def __init__(self):
        self.running = True
        self.inventory_manager = InventoryManager()  # Initialize InventoryManager

    def main_menu(self):
        print(Style.BRIGHT + Fore.CYAN + "Timeless Final Fantasy XI Toolbox")
        print(Fore.CYAN + "Main Menu\n")
        print(Fore.GREEN + "1. Auction House")
        print(Fore.GREEN + "2. Mailbox")
        print(Fore.GREEN + "3. Inventory Management")  # New Inventory Management Option
        print(Fore.RED + "4. Exit")
        choice = input(Fore.YELLOW + "Please select an option: ")
        return choice

    def auction_house_menu(self):
        while True:
            print(Fore.CYAN + "Welcome to the Auction House!")
            print(Fore.YELLOW + "1. Update Auction House")
            print(Fore.YELLOW + "2. Buy All Items")
            print(Fore.YELLOW + "3. Buy Random Items")
            print(Fore.RED + "4. Return to Main Menu")
            choice = input(Fore.YELLOW + "Please select an option: ")
            if choice == "1":
                update_auction_house()
            elif choice == "2":
                buy_all_items()
            elif choice == "3":
                buy_random_items()
            elif choice == "4":
                break  # Exit the loop to return to main menu
            else:
                print(Fore.RED + "Invalid option")

    def mailbox_menu(self):
        while True:
            print(Fore.CYAN + "Welcome to the Mailbox!")
            deliver_instance = (
                deliver.Deliver()
            )  # Create an instance of Deliver directly
            print(Fore.YELLOW + "1. Send item to a single character")
            print(Fore.YELLOW + "2. Send item to multiple characters")
            print(Fore.YELLOW + "3. Send an item to all characters")
            print(Fore.RED + "4. Return to Main Menu")
            mode = input(Fore.YELLOW + "Please select an option: ")
            if mode == "1":
                deliver_instance.interact_with_user(mode="single")
            elif mode == "2":
                deliver_instance.interact_with_user(mode="multiple")
            elif mode == "3":
                deliver_instance.interact_with_user(mode="all")
            elif mode == "4":
                break  # Exit the loop to return to main menu
            else:
                print(Fore.RED + "Invalid option")

    def inventory_menu(self):
        while True:
            print(Fore.CYAN + "Welcome to Inventory Management!")
            print(Fore.YELLOW + "1. Print Character Inventory")
            print(
                Fore.YELLOW + "2. Add Item to Character Inventory"
            )  # New option for adding an item
            print(Fore.RED + "3. Return to Main Menu")
            choice = input(Fore.YELLOW + "Please select an option: ")
            if choice == "1":
                char_name = input(Fore.YELLOW + "Enter character name: ")
                self.inventory_manager.print_inventory(char_name)
            elif choice == "2":
                char_name = input(Fore.YELLOW + "Enter character name: ")
                char_id = self.inventory_manager.get_char_id(char_name)
                if char_id is not None:
                    item_id = int(input(Fore.YELLOW + "Enter item ID: "))
                    quantity = int(input(Fore.YELLOW + "Enter quantity: "))
                    self.inventory_manager.add_item_to_inventory(
                        char_id, item_id, quantity
                    )
                else:
                    print(Fore.RED + "Character not found.")
            elif choice == "3":
                break
            else:
                print(Fore.RED + "Invalid option")

    def run(self):
        while self.running:
            choice = self.main_menu()
            if choice == "1":
                self.auction_house_menu()
            elif choice == "2":
                self.mailbox_menu()
            elif choice == "3":
                self.inventory_menu()
            elif choice == "4":
                print(Fore.GREEN + "Goodbye!")
                self.running = False
            else:
                print(Fore.RED + "Invalid option")


if __name__ == "__main__":
    toolbox = GameToolbox()
    toolbox.run()

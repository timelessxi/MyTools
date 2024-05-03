from colorama import init, Fore, Style

# Set up colorama for colored output.
init(autoreset=True)

# Import modules
from delivery_box import deliver
from auction_house import update_auction_house, buy_all_items, buy_random_items
from inventory_manager import InventoryManager
from database import database
import sys


class GameToolbox:
    def __init__(self):
        # Keep the game running until told to stop.
        self.running = True
        # Set up an inventory manager for handling item inventories.
        self.inventory_manager = InventoryManager()

    def main_menu(self):
        # Main menu actions mapped to their corresponding functions.
        menu_options = {
            "1": self.auction_house_menu,
            "2": self.mailbox_menu,
            "3": self.inventory_menu,
            "4": self.exit_program,
        }
        while True:
            # Display the main menu.
            print(Style.BRIGHT + Fore.CYAN + "Timeless Final Fantasy XI Toolbox")
            print(Fore.CYAN + "Main Menu\n")
            print(Fore.GREEN + "1. Auction House")
            print(Fore.GREEN + "2. Mailbox")
            print(Fore.GREEN + "3. Inventory Management")
            print(Fore.RED + "4. Exit")

            # Get user choice and execute the corresponding action.
            choice = input(Fore.YELLOW + "Please select an option: ")
            action = menu_options.get(choice, lambda: None)
            if action and action() == True:
                return

    def exit_program(self):
        # Exit the program cleanly.
        print(Fore.GREEN + "Goodbye!")
        self.running = False
        return True

    def auction_house_menu(self):
        # Menu for auction house options.
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
                break
            else:
                print(Fore.RED + "Invalid option")

    def mailbox_menu(self):
        # Menu for managing the delivery box.
        while True:
            print(Fore.CYAN + "Welcome to the Mailbox!")
            deliver_instance = deliver.Deliver()
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
                break
            else:
                print(Fore.RED + "Invalid option")

    def inventory_menu(self):
        # Menu for inventory management.
        while True:
            print(Fore.CYAN + "Welcome to Inventory Management!")
            print(Fore.YELLOW + "1. Print Character Inventory")
            print(Fore.YELLOW + "2. Add Item to Character Inventory")
            print(Fore.RED + "3. Return to Main Menu")
            choice = input(Fore.YELLOW + "Please select an option: ")
            if choice == "1":
                char_name = input(Fore.YELLOW + "Enter character name: ")
                self.inventory_manager.print_inventory(char_name)
            elif choice == "2":
                char_name = input(Fore.YELLOW + "Enter character name: ")
                char_id = self.inventory_manager.get_char_id(char_name)
                if char_id is not None:
                    try:
                        item_id = int(input(Fore.YELLOW + "Enter item ID: "))
                        quantity = int(input(Fore.YELLOW + "Enter quantity: "))
                        self.inventory_manager.add_item_to_inventory(
                            char_id, item_id, quantity
                        )
                    except ValueError:
                        print(
                            Fore.RED
                            + "Please enter valid integers for item ID and quantity."
                        )
                else:
                    print(Fore.RED + "Character not found.")
            elif choice == "3":
                break
            else:
                print(Fore.RED + "Invalid option")

    def run(self):
        # Start the application and handle any critical errors.
        try:
            database.init_connection_pool()
            if database.pool is None:
                raise Exception("Database connection pool could not be initialized.")
            while self.running:
                self.main_menu()
                if not self.running:
                    break
        except Exception as e:
            print(f"Critical error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    toolbox = GameToolbox()
    toolbox.run()

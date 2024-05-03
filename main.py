from colorama import init, Fore, Style
import sys

# Set up colorama for colored output.
init(autoreset=True)

# Import modules
from delivery_box import deliver
from auction_house import update_auction_house, buy_all_items, buy_random_items
from inventory_manager import InventoryManager
from database import database
import logging

# Setup basic logging
logging.basicConfig(filename='game_toolbox.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

class GameToolbox:
    def __init__(self):
        self.running = True
        self.inventory_manager = InventoryManager()

    def validate_input(self, prompt, choice_type=int):
        while True:
            try:
                user_input = input(prompt)
                return choice_type(user_input)
            except ValueError:
                print(Fore.RED + f"Invalid input. Please enter a valid {choice_type.__name__}.")

    def main_menu(self):
        menu_options = {
            1: self.auction_house_menu,
            2: self.mailbox_menu,
            3: self.inventory_menu,
            4: self.exit_program,
        }
        while self.running:
            if not database.check_database_exists("xidb") or not database.check_database_exists("ah_data"):
                logging.error("One or more required databases are missing.")
                print(Fore.RED + "One or more required databases are missing. Exiting.")
                sys.exit(1)

            print(Style.BRIGHT + Fore.CYAN + "Timeless Final Fantasy XI Toolbox")
            print(Fore.CYAN + "Main Menu\n")
            print(Fore.GREEN + "1. Auction House")
            print(Fore.GREEN + "2. Mailbox")
            print(Fore.GREEN + "3. Inventory Management")
            print(Fore.RED + "4. Exit")

            choice = self.validate_input(Fore.YELLOW + "Please select an option (1-4): ", int)
            action = menu_options.get(choice, None)
            if action:
                action()
            else:
                print(Fore.RED + "Invalid option. Please choose from 1 to 4.")

    def exit_program(self):
        print(Fore.GREEN + "Goodbye!")
        self.running = False

    def auction_house_menu(self):
        while True:
            print(Fore.CYAN + "Welcome to the Auction House!")
            print(Fore.YELLOW + "1. Update Auction House")
            print(Fore.YELLOW + "2. Buy All Items")
            print(Fore.YELLOW + "3. Buy Random Items")
            print(Fore.RED + "4. Return to Main Menu")

            choice = self.validate_input(Fore.YELLOW + "Please select an option (1-4): ", int)
            if choice == 1:
                update_auction_house()
            elif choice == 2:
                buy_all_items()
            elif choice == 3:
                buy_random_items()
            elif choice == 4:
                break
            else:
                print(Fore.RED + "Invalid option")

    def mailbox_menu(self):
        while True:
            print(Fore.CYAN + "Welcome to the Mailbox!")
            deliver_instance = deliver.Deliver()
            print(Fore.YELLOW + "1. Send item to a single character")
            print(Fore.YELLOW + "2. Send item to multiple characters")
            print(Fore.YELLOW + "3. Send an item to all characters")
            print(Fore.RED + "4. Return to Main Menu")

            mode = self.validate_input(Fore.YELLOW + "Please select an option (1-4): ", int)
            if mode == 1:
                deliver_instance.interact_with_user(mode="single")
            elif mode == 2:
                deliver_instance.interact_with_user(mode="multiple")
            elif mode == 3:
                deliver_instance.interact_with_user(mode="all")
            elif mode == 4:
                break
            else:
                print(Fore.RED + "Invalid option")


    def inventory_menu(self):
        while True:
            print(Fore.CYAN + "Welcome to Inventory Management!")
            print(Fore.YELLOW + "1. Print Character Inventory")
            print(Fore.YELLOW + "2. Add Item to Character Inventory")
            print(Fore.RED + "3. Return to Main Menu")

            choice = self.validate_input(Fore.YELLOW + "Please select an option (1-3): ", int)
            if choice == 1:
                char_name = input(Fore.YELLOW + "Enter character name: ")
                self.inventory_manager.print_inventory(char_name)
            elif choice == 2:
                char_name = input(Fore.YELLOW + "Enter character name: ")
                char_id = self.inventory_manager.get_char_id(char_name)
                if char_id is not None:
                    item_id = self.validate_input(Fore.YELLOW + "Enter item ID: ", int)
                    quantity = self.validate_input(Fore.YELLOW + "Enter quantity: ", int)
                    self.inventory_manager.add_item_to_inventory(char_id, item_id, quantity)
                else:
                    print(Fore.RED + "Character not found.")
            elif choice == 3:
                break
            else:
                print(Fore.RED + "Invalid option")

    def run(self):
        try:
            database.init_connection_pool()
            if database.pool is None:
                raise Exception("Database connection pool could not be initialized.")
            self.main_menu()
        except Exception as e:
            logging.error(f"Critical error: {e}")
            print(Fore.RED + f"Critical error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    toolbox = GameToolbox()
    toolbox.run()

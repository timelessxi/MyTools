from colorama import init, Fore, Style
import sys
import logging
from auction_house.auction import AuctionHouseManager
from inventory_manager import InventoryManager
from database import database
from menus.auction_house_menu import auction_house_menu
from menus.mailbox_menu import mailbox_menu
from menus.inventory_menu import inventory_menu

init(autoreset=True)
logging.basicConfig(
    filename="game_toolbox.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


class GameToolbox:
    def __init__(self):
        self.running = True
        self.inventory_manager = InventoryManager()
        self.auction_manager = AuctionHouseManager()

    def validate_input(self, prompt, choice_type=int):
        while True:
            try:
                user_input = input(prompt)
                return choice_type(user_input)
            except ValueError:
                print(
                    Fore.RED
                    + f"Invalid input. Please enter a valid {choice_type.__name__}."
                )

    def main_menu(self):
        menu_options = {
            1: lambda: auction_house_menu(self.auction_manager, self.validate_input),
            2: lambda: mailbox_menu(self.validate_input),
            3: lambda: inventory_menu(self.inventory_manager, self.validate_input),
            4: self.exit_program,
        }
        while self.running:
            if not database.check_database_exists(
                "xidb"
            ) or not database.check_database_exists("ah_data"):
                logging.error("One or more required databases are missing.")
                print(Fore.RED + "One or more required databases are missing. Exiting.")
                sys.exit(1)

            print(Style.BRIGHT + Fore.CYAN + "Timeless Final Fantasy XI Toolbox")
            print(Fore.CYAN + "Main Menu\n")
            print(Fore.GREEN + "1. Auction House")
            print(Fore.GREEN + "2. Mailbox")
            print(Fore.GREEN + "3. Inventory Management")
            print(Fore.RED + "4. Exit")

            choice = self.validate_input(
                Fore.YELLOW + "Please select an option (1-4): ", int
            )
            action = menu_options.get(choice, None)
            if action:
                action()
            else:
                print(Fore.RED + "Invalid option. Please choose from 1 to 4.")

    def exit_program(self):
        print(Fore.GREEN + "Goodbye!")
        self.running = False

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

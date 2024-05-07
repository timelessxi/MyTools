from colorama import Fore


def auction_house_menu(auction_manager, validate_input):
    while True:
        print(Fore.CYAN + "Welcome to the Auction House!")
        print(Fore.YELLOW + "1. Update Auction House")
        print(Fore.YELLOW + "2. Buy All Items")
        print(Fore.YELLOW + "3. Buy Random Items")
        print(Fore.RED + "4. Return to Main Menu")

        choice = validate_input(Fore.YELLOW + "Please select an option (1-4): ", int)
        if choice == 1:
            auction_manager.update_auction_house()
        elif choice == 2:
            auction_manager.buy_all_items()
        elif choice == 3:
            auction_manager.buy_random_items()
        elif choice == 4:
            break
        else:
            print(Fore.RED + "Invalid option")

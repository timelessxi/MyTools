from colorama import Fore

def inventory_menu(inventory_manager, validate_input):
    while True:
        print(Fore.CYAN + "Welcome to Inventory Management!")
        print(Fore.YELLOW + "1. Print Character Inventory")
        print(Fore.YELLOW + "2. Add Item to Character Inventory")
        print(Fore.RED + "3. Return to Main Menu")

        choice = validate_input(Fore.YELLOW + "Please select an option (1-3): ", int)
        if choice == 1:
            char_name = input(Fore.YELLOW + "Enter character name: ")
            inventory_manager.print_inventory(char_name)
        elif choice == 2:
            char_name = input(Fore.YELLOW + "Enter character name: ")
            char_id = inventory_manager.get_char_id(char_name)
            if char_id is not None:
                item_id = validate_input(Fore.YELLOW + "Enter item ID: ", int)
                quantity = validate_input(Fore.YELLOW + "Enter quantity: ", int)
                inventory_manager.add_item_to_inventory(char_id, item_id, quantity)
            else:
                print(Fore.RED + "Character not found.")
        elif choice == 3:
            break
        else:
            print(Fore.RED + "Invalid option")

from colorama import Fore
from delivery_box import deliver


def mailbox_menu(validate_input):
    while True:
        print(Fore.CYAN + "Welcome to the Mailbox!")
        deliver_instance = deliver.Deliver()
        print(Fore.YELLOW + "1. Send item to a single character")
        print(Fore.YELLOW + "2. Send item to multiple characters")
        print(Fore.YELLOW + "3. Send an item to all characters")
        print(Fore.RED + "4. Return to Main Menu")

        mode = validate_input(Fore.YELLOW + "Please select an option (1-4): ", int)
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

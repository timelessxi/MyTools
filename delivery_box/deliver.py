from database.database import execute_query


class Deliver:
    def __init__(self):
        pass

    def get_charid(self, charname):
        query = "SELECT charid FROM chars WHERE charname = %s"
        result = execute_query(query, params=(charname,), fetch=True)
        return result[0][0] if result else None

    def get_all_charids(self):
        query = "SELECT charid FROM chars"
        results = execute_query(query, fetch=True)
        return [result[0] for result in results] if results else []

    def search_items(self, item_name):
        tables = [
            "item_equipment",
            "item_basic",
            "item_furnishing",
            "item_puppet",
            "item_weapon",
        ]
        results = []
        for table in tables:
            query = f"SELECT itemid, name FROM {table} WHERE name LIKE %s"
            fetched_items = execute_query(query, params=(f"%{item_name}%",), fetch=True)
            if fetched_items:
                results.extend(fetched_items)
        return results

    def send_item(self, charid, itemid, quantity):
        query = """
        INSERT INTO delivery_box
        (charid, charname, box, slot, itemid, itemsubid, quantity, extra, senderid, sender, received, sent)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        data = (charid, None, 1, 0, itemid, 0, quantity, None, 0, "MHMU", 0, 0)
        execute_query(query, params=data, commit=True)

    def interact_with_user(self, mode="single"):
        charids = []
        if mode == "all":
            charids = self.get_all_charids()
            if not charids:
                print("No characters found.")
                return
        elif mode == "multiple":
            charnames = input("Enter the names of the characters separated by commas (e.g., John, Jane, Doe): ")
            charnames = [name.strip() for name in charnames.split(',')]
            charids = [self.get_charid(name) for name in charnames if self.get_charid(name)]
            if not charids:
                print("One or more characters not found.")
                return
        else:  # single mode
            charname = input("Enter the character's name: ")
            charid = self.get_charid(charname)
            if charid is None:
                print("Character not found.")
                return
            charids.append(charid)

        item_name = input("Enter the item name (full or partial): ")
        items = self.search_items(item_name)
        if not items:
            print("No items found.")
            return

        print("Found items:")
        for index, (itemid, name) in enumerate(items):
            print(f"{index + 1}. {name.title().replace('_', ' ')}")

        item_choice = int(input("Select the item number to send: ")) - 1
        if item_choice < 0 or item_choice >= len(items):
            print("Invalid item selection.")
            return

        selected_item = items[item_choice]
        quantity = int(input("Enter the quantity to send: "))

        for charid in charids:
            if charid:
                self.send_item(charid, selected_item[0], quantity)

        if mode == "all":
            print(f"Sent {quantity} {selected_item[1].title().replace('_', ' ')} to all characters.")




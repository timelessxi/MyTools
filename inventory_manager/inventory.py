import pandas as pd
import logging
from database.database import execute_query


class InventoryManager:
    def __init__(self):
        # Initializes the InventoryManager class.
        pass

    def get_char_id(self, char_name):
        # Retrieves the character ID based on the character name.
        query = "SELECT charid FROM chars WHERE charname = %s;"
        result = execute_query(query, params=(char_name,), fetch=True, database="xidb")
        if result:
            return result[0][0]  # Return the first result's ID.
        return None

    def get_inventory(self, char_id):
        # Fetches the inventory for a given character ID.
        query = "SELECT itemid, quantity FROM char_inventory WHERE charid = %s;"
        results = execute_query(query, params=(char_id,), fetch=True, database="xidb")
        return results

    def get_item_names(self, item_ids):
        # Gets the names of items based on their IDs.
        if not item_ids:
            return {}
        format_strings = ",".join(["%s"] * len(item_ids))
        query = (
            f"SELECT itemid, name FROM item_basic WHERE itemid IN ({format_strings});"
        )
        results = execute_query(query, params=item_ids, fetch=True, database="xidb")
        return {itemid: name.title().replace("_", " ") for itemid, name in results}

    def print_inventory(self, char_name):
        # Prints the inventory of a character.
        char_id = self.get_char_id(char_name)
        if char_id:
            inventory = self.get_inventory(char_id)
            item_ids = [item[0] for item in inventory]  # Extract item IDs.
            item_names = self.get_item_names(item_ids)  # Get item names.
            inventory_list = [
                {
                    "Item Name": item_names.get(itemid, "Unknown Item"),
                    "Quantity": quantity,
                }
                for itemid, quantity in inventory
            ]
            inventory_df = pd.DataFrame(inventory_list)
            if not inventory_df.empty:
                pd.set_option("display.max_rows", None)
                pd.set_option("display.max_columns", None)
                pd.set_option("display.expand_frame_repr", False)
                pd.set_option("display.colheader_justify", "left")
                print(inventory_df.to_string(index=False))
            else:
                print("No items found in inventory.")
        else:
            print("Character not found.")

    # Set up logging for debugging and tracking operations.
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    def add_item_to_inventory(self, char_id, item_id, quantity):
        # Adds an item to the inventory of a character.
        logging.debug(
            f"Attempting to add item: {item_id} with quantity: {quantity} to char_id: {char_id}"
        )

        # Query to find the max slots from character storage.
        storage_query = "SELECT inventory FROM char_storage WHERE charid = %s;"
        try:
            storage_result = execute_query(storage_query, params=(char_id,), fetch=True)
            max_slots = storage_result[0][0]
            logging.debug(f"Maximum slots retrieved: {max_slots}")
        except Exception as e:
            logging.error(f"Failed to retrieve storage information: {e}")
            return

        # Query to find the next available slot in the inventory.
        inventory_query = "SELECT COALESCE(MAX(slot) + 1, 0) AS next_slot FROM char_inventory WHERE charid = %s AND location = 0;"
        try:
            inventory_result = execute_query(
                inventory_query, params=(char_id,), fetch=True
            )
            next_slot = inventory_result[0][0]
            logging.debug(f"Next available slot: {next_slot}")
            if next_slot >= max_slots:
                logging.warning("Inventory is full or exceeds max slots.")
                return
        except Exception as e:
            logging.error(f"Error finding next available slot: {e}")
            return

        # Insert the new item into the inventory.
        insert_query = "INSERT INTO char_inventory (charid, location, slot, itemid, quantity) VALUES (%s, 0, %s, %s, %s);"
        try:
            execute_query(
                insert_query,
                params=(char_id, next_slot, item_id, quantity),
                commit=True,
                database="xidb",
            )
            logging.info(
                "Item added successfully. Player will need to zone or relog to see the changes."
            )
        except Exception as e:
            logging.error(f"Failed to add item: {e}")

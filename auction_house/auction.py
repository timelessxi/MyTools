import random
import time
import logging
from database.database import execute_query


class AuctionHouseManager:
    # Map item rates to their required quantities in the auction house.
    rate_mapping = {
        "Dead Slow": 2,
        "Very Slow": 2,
        "Slow": 3,
        "Average": 5,
        "Fast": 8,
        "Very Fast": 8,
    }

    # Generate a random name from a predefined list for auction item buyers and sellers.
    name_list = [
        "Aelar",
        "Brondar",
        "Caelum",
        "Draka",
        "Eilora",
        "Fenris",
        "Gorim",
        "Helia",
        "Ithra",
        "Jorund",
        "Kyra",
        "Lorin",
        "Mirelle",
        "Narlok",
        "Ophira",
        "Pyralis",
        "Quinlan",
        "Rael",
        "Sylvana",
        "Torin",
        "Ulyra",
        "Vaelis",
        "Wyran",
        "Xyrella",
        "Yorith",
        "Zephyra",
    ]

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG)

    def get_name(self):
        return random.choice(self.name_list)

    def buy_random_items(self):
        print("Buying random items...")
        current_time = int(time.time())
        all_items = execute_query(
            "SELECT id, price FROM auction_house WHERE sell_date = 0",
            fetch=True,
            database="xidb",
        )
        if not all_items:
            print("No items available for purchase.")
            return

        num_items_to_buy = max(len(all_items) // 5, 1)
        items_to_buy = random.sample(all_items, k=num_items_to_buy)
        for item in items_to_buy:
            execute_query(
                "UPDATE auction_house SET buyer_name = %s, sale = %s, sell_date = %s WHERE id = %s AND sell_date = 0",
                (self.get_name(), item[1], current_time, item[0]),
                commit=True,
                database="xidb",
            )
        print(f"Randomly purchased items: {len(items_to_buy)}")
        print("\n")

    def buy_all_items(self):
        print("Buying all items...")
        current_time = int(time.time())
        items_for_sale = execute_query(
            "SELECT id, price FROM auction_house WHERE sell_date = 0",
            fetch=True,
            database="xidb",
        )
        if not items_for_sale:
            print("No items available for purchase.")
            return

        for item in items_for_sale:
            execute_query(
                "UPDATE auction_house SET buyer_name = %s, sale = %s, sell_date = %s WHERE id = %s AND sell_date = 0",
                (self.get_name(), item[1], current_time, item[0]),
                commit=True,
                database="xidb",
            )
        print(f"Purchased all items: {len(items_for_sale)}")
        print("\n")

    def update_auction_house(self):
        print("Updating auction house... This may take a few moments.")
        try:
            items_query = "SELECT itemid, stack_price, single_price, rate FROM items"
            items = execute_query(items_query, fetch=True, database="ah_data")

            for item in items:
                item_id, stack_price, single_price, rate = item

                # Process single item prices
                if single_price > 0:
                    self.process_item(item_id, 0, single_price, rate, "xidb")

                # Process stack item prices only if stack_price is greater than 0
                if stack_price > 0:
                    self.process_item(item_id, 1, stack_price, rate, "xidb")

            print("Auction house updated successfully.")
            print("\n")
        except Exception as e:
            logging.error("Failed to update auction house: %s", e)

    def process_item(self, item_id, stack, price, rate, database):
        required_quantity = self.rate_mapping.get(rate, 3)
        current_time = int(time.time())
        current_qty = self.check_existing_quantity(item_id, stack, database)
        qty_to_add = required_quantity - current_qty

        for _ in range(qty_to_add):
            execute_query(
                "INSERT INTO auction_house (itemid, stack, seller, seller_name, date, price, buyer_name, sale, sell_date) VALUES (%s, %s, 0, %s, %s, %s, NULL, 0, 0)",
                (item_id, stack, self.get_name(), current_time, price),
                commit=True,
                database=database,
            )

    def check_existing_quantity(self, item_id, stack, database):
        result = execute_query(
            "SELECT COUNT(*) FROM auction_house WHERE itemid = %s AND stack = %s AND sell_date = 0",
            (item_id, stack),
            fetch=True,
            database=database,
        )
        return result[0][0] if result else 0

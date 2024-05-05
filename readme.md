# Tools for FFXI Private Server


This toolbox is designed to enhance the functionality of the Final Fantasy XI server emulator by LandSandBoat. It provides a suite of tools for managing the auction house, mailing items to players, and character inventories, directly interfacing with the xidb database to perform these operations.

## Features

- **Auction House Management**: Automate auction house transactions, including item purchases and price updates.
- **Delivery System**: Facilitate the delivery of items to characters within the game.
- **Inventory Management**: Manage the inventories of characters, including adding and viewing characters' current inventory.
- **Seamless Integration**: Designed to work seamlessly with the LandSandBoat server emulator's database schema.

## Prerequisites

- Python 3.6+
- MySQL Server
- [LandSandBoat/server](https://github.com/LandSandBoat/server) FFXI server emulator setup and running
- Virtual Environment (recommended)

## Installation

1. Ensure the LandSandBoat server emulator is installed and properly configured.
2. Clone the TimelessToolbox repository:
   ```bash
   git clone https://github.com/timelessxi/TimelessToolbox.git
3. Navigate to the TimelessToolbox directory and install dependencies:
    ```bash
   cd TimelessToolbox
   pip install -r requirements.txt
   ```

## Configuration

Before running TimelessToolbox, you'll need to set up your configuration file:

1. Navigate to the `config` directory within the TimelessToolbox project.
2. Create a new file named `config.json`.
3. Structure your `config.json` file as follows, replacing the placeholders with your actual database connection details:
   ```json
   {
       "host": "localhost",
       "user": "your_database_user",
       "password": "your_database_password",
       "database": "xidb"
     }
   ```

This file contains sensitive information, such as your database password, which is why it is not included in the repository and listed in `.gitignore`.

## Auction House Data Setup

The functionality of the update_auction_house tool depends on the ah_data database, which contains critical information about item prices.

### Importing the ah_data Database

A SQL dump of the ah_data database is provided in the /auction/assets directory. To import this data into your system, follow these steps:

- **Ensure MariaDB/MySQL is installed**: This step should have been completed during the initial server setup.
- **Create the Database**:
  If the ah_data database does not exist, create it using the following command:
  ```bash
  mysql -u root -p -e "CREATE DATABASE ah_data"
  ```

### Import the Database

- Navigate to the directory containing ah_data.sql.
- Run the following command to import the database:
  ```bash
  mysql -u root -p ah_data < ah_data.sql
  ```

## Running The Program

Execute the main script to access the toolbox:

```bash
python main.py
```

Follow the on-screen prompts to interact with the auction house, delivery system, and inventory management tools.

## Integration with LandSandBoat Server

TimelessToolbox directly interacts with the MySQL database used by the LandSandBoat server emulator. Ensure that any operations performed through MyTools are compatible with your server's version and configuration. Regularly backup your database to prevent data loss or corruption.

## Contributing

Contributions to both TimelessToolbox and the LandSandBoat server emulator are welcome. Please adhere to each project's contribution guidelines.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

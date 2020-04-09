# Poppi-QTpi
Poppi QTπ is my all-in-one Discord bot with RP GIFs, moderation utilities and much more!

## Usage
To use Poppi QTπ, you can either use python directly or use the automatically built docker image!

### Using Python directly
To use Python directly, make sure you have Python 3.8 or newer and then follow these steps:
- Install required pip libraries by doing `pip install -r requirements.txt` in the root folder
- Set the `POPPI_TOKEN, PREFIX, VERSION` environment variables to the bot's token, the prefix you want, the current version (as specified in docker-compose.yml) and your Discord ID
- Run the bot with `python ./src/main.py`

### Using Docker
To use Docker (the recommended way of using Poppi QTπ) follow these steps:
- Set the `POPPI_TOKEN` environment variable to the bot's token and your Discord ID
- Run `docker-compose up -d`
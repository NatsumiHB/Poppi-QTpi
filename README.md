# Poppi-QTpi
[![Actions Status](https://github.com/NatsumiHB/Poppi-QTpi/workflows/Build%20and%20Push%20to%20Docker/badge.svg)](https://github.com/NatsumiHB/Poppi-QTpi/actions)

Poppi QTπ is my all-in-one Discord bot with RP GIFs, moderation utilities and much more!

**Current Version: 1.3**

## Usage
To use Poppi QTπ, follow these steps:
#### To use Python directly, make sure you have Python 3.8 or newer and then follow these steps:
1. Install required pip libraries by doing `pip install -r requirements.txt` in the root folder
2. Set the `POPPI_TOKEN, POPPI_DBL_TOKEN, POPPI_PREFIX, POPPI_VERSION` environment variables to the bot's token, your Discord Bot List token, the prefix you want and the current version
3. Run the bot with `python ./src/main.py`

#### To use Docker follow these steps:
1. Set the same environmental variables as in the Python guide
2. Run `docker-compose up -d`

**The standard docker-compose comes with watchtower to automatically update your Poppi QTπ instance when a new version is released**
# Poppi-QTpi
[![Actions Status](https://github.com/NatsumiHB/Poppi-QTpi/workflows/Build%20and%20Push%20to%20Docker/badge.svg)](https://github.com/NatsumiHB/Poppi-QTpi/actions)

![Poppi QTπ avatar](https://images.discordapp.net/avatars/430092067218128916/30f9a115a465fd5a523c332398ccea84.png)

Poppi QTπ is my all-in-one Discord bot with RP GIFs, moderation utilities and much more!

## Usage
To use Poppi QTπ, follow these steps:

#### To use Python directly, make sure you have Python 3.8 or newer and then follow these steps:
1. Install required pip libraries by doing `pip install -r requirements.txt` in the root folder
2. Set the `POPPI_TOKEN, POPPI_DBL_TOKEN, POPPI_PREFIX and POPPI_OWNER_ID` environment variables to the bot's token,
your Discord Bot List token, the prefix you want and the current version
3. Run the bot with `python ./src/main.py`

**Alternatively, you can use pipenv! For that install the libraries with `pipenv install -r requirements.txt`
and then run the bot with `pipenv run python ./src/main.py`**

#### To use Docker follow these steps:
1. Set the same environment variables as in the Python guide
2. Run `docker-compose up -d` (or without `-d` if you do not want the bot to run as a daemon)

#### If you wish to run Poppi QTπ without some specific environment variables set, you can refer to this table to make the needed code changes:
| Variable            | Where                                 |
| :-----------------: | :-----------------------------------: |
| **POPPI_TOKEN**     | main.py                               |
| **POPPI_PREFIX**    | main.py                               |
| **POPPI_OWNER_ID**  | main.py; cogs/help_and_information.py |
| **POPPI_DBL_TOKEN** | cogs/TopGG.py                         |

## Credits
##### This bot uses the FetchedUser class from [RoboDanny](https://github.com/Rapptz/RoboDanny/blob/18b92ae2f53927aedebc25fb5eca02c8f6d7a874/cogs/meta.py#L21). 
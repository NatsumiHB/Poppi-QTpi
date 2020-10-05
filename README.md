# Poppi-QTpi
[![Actions Status](https://github.com/NatsumiHB/Poppi-QTpi/workflows/Publish%20Docker%20image/badge.svg)](https://github.com/NatsumiHB/Poppi-QTpi/actions)

![Poppi QTπ avatar](https://api.poppi-bot.xyz/avatar)

Poppi QTπ is my all-in-one Discord bot with RP GIFs, moderation utilities and much more!

## Usage
To use Poppi QTπ, follow these steps:

#### To use Python directly, make sure you have Python 3.8 or newer and then follow these steps:
**For all of these you need to set the required environment variables in the `.env` file**

1. Install required pip libraries by doing `pip install -r requirements.txt` in the root folder
2. Run the bot with `python ./main.py` inside of `/src`

**Alternatively, you can use pipenv! For that install the libraries with `pipenv install -r requirements.txt`
and then run the bot with `pipenv run python ./src/main.py`**

#### To use Docker do this:
You can just run the image (`natsuwumi/poppi`*). Make sure to set the required environmental variables/`.env` file in your docker command/compose file.

**Keep in mind that docker-compose's `.env` support does not properly work with variables that end in a whitespace.**

The API runs on port 5000, so if you wish to use that make sure to publish that port.

*Alternatively, you can use the same image hosted on GitHub's Container Registry (check the packages tab for instructions)

#### If you wish to run Poppi QTπ without some specific environment variables set, you can refer to this table to make the needed code changes:
| Variable            | Where                                 |
| :-----------------: | :-----------------------------------: |
| **POPPI_TOKEN**     | main.py                               |
| **POPPI_PREFIX**    | main.py                               |
| **POPPI_OWNER_ID**  | main.py; cogs/help_and_information.py |
| **POPPI_DBL_TOKEN** | cogs/TopGG.py                         |

#### API Endpoints
| Endpoint      | Result                              |
| :-----------: | :---------------------------------: |
| /server_count | Amount of servers as normal text    |
| /avatar       | Redirect to the bot's avatar        |
| /commands     | JSON of all commands and categories |

## Credits
-  FetchedUser class from [RoboDanny](https://github.com/Rapptz/RoboDanny/blob/18b92ae2f53927aedebc25fb5eca02c8f6d7a874/cogs/meta.py#L21). 

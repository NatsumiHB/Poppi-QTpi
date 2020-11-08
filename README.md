# Poppi-QTpi
[![Actions Status](https://github.com/NatsumiHB/Poppi-QTpi/workflows/Publish%20Docker%20image/badge.svg)](https://github.com/NatsumiHB/Poppi-QTpi/actions)

![Poppi QTπ avatar](https://api.poppi-bot.xyz/avatar | width=256)

Poppi QTπ is my all-in-one Discord bot with RP GIFs, moderation utilities and much more!

## Usage
To use Poppi QTπ, follow these steps:

#### To use Python directly, make sure you have Python 3.9 or newer and then follow these steps:
1. Install required pip libraries by doing `pip install -r requirements.txt` in the root folder
2. Run the bot with `python ./main.py` inside of `/src`

**Alternatively, you can use pipenv! For that install the libraries with `pipenv install -r requirements.txt`
and then run the bot with `pipenv run python ./src/main.py`**

#### To use Docker do this:
You can just run the image (`natsuwumi/poppi`*). Make sure to set to configure Poppi QTπ with a configuration file as per this documentation.

The API runs on port 5000, so if you wish to use that make sure to publish that port.

#### Configuring Poppi QTπ
# TODO
```json
{
  "prefix": "",
  "owner_id": 0,
  "token": "",
  "dbl_token": "",

  "db_password": "",
  "db_hostname": "",

  "currency": "",

  "empty_profile": {
    "nickname": null,
    "description": null,
    "avatar_url": null,
    "last_daily": null,
    "money": 0
  }
}
```

#### If you wish to run Poppi QTπ without some specific configuration variables set, you can refer to this table to make the needed code changes:
| Variable      | Where                                 |
| :-----------: | :-----------------------------------: |
| **token**     | main.py                               |
| **prefix**    | main.py                               |
| **owner_id**  | main.py; cogs/help_and_information.py |
| **dbl_token** | cogs/TopGG.py                         |

#### API Endpoints
| Endpoint      | Result                              |
| :-----------: | :---------------------------------: |
| /server_count | Amount of servers as normal text    |
| /avatar       | Redirect to the bot's avatar        |
| /commands     | JSON of all commands and categories |

## Credits
-  FetchedUser class from [RoboDanny](https://github.com/Rapptz/RoboDanny/blob/18b92ae2f53927aedebc25fb5eca02c8f6d7a874/cogs/meta.py#L21). 

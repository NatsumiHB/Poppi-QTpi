# Poppi-QTpi

[![Actions Status](https://github.com/NatsumiHB/Poppi-QTpi/workflows/Publish%20Docker%20image/badge.svg)](https://github.com/NatsumiHB/Poppi-QTpi/actions)

<img src="https://api.poppi-bot.xyz/avatar" alt="Poppi QTπ avatar" width="256" height="256">

Poppi QTπ is my all-in-one Discord bot with RP GIFs, moderation utilities and much more!

## Usage

To use Poppi QTπ, follow these steps:

**No matter how you run Poppi QTπ, you will need to run an instance of ArangoDB (for non-Docker deployments it will need
to run on the default port (8529))**

#### To use Python directly, make sure you have Python 3.9 or newer and then follow these steps:

1. Install required pip libraries by doing `pip install -r requirements.txt` in the root folder
2. Run the bot with `python ./main.py` inside of `/src`

**Alternatively, you can use pipenv! For that install the libraries with `pipenv install -r requirements.txt`
and then run the bot with `pipenv run python ./src/main.py`**

#### To use Docker do this:

You can just run the image (`natsuwumi/poppi`). Make sure to mount the config file for Poppi QTπ
to `/srv/poppi/config.json`.

The API runs on port 5000, so if you wish to use that make sure to publish that port.

#### Configuring Poppi QTπ

Set the empty fields in the `config.json` file to your likings. You may also change defaults for profiles/money and
store items in their respective files.

If you do not have a DBL token you can set it to `debug` to disable DBL updates.

If you have any questions, feel free to [open an issue](https://github.com/NatsumiHB/Poppi-QTpi/issues).

#### API Endpoints

| Endpoint      | Result                              |
| :-----------: | :---------------------------------: |
| /server_count | Amount of servers as normal text    |
| /avatar       | Redirect to the bot's avatar        |
| /commands     | JSON of all commands and categories |

## Credits

- FetchedUser class
  from [RoboDanny](https://github.com/Rapptz/RoboDanny/blob/18b92ae2f53927aedebc25fb5eca02c8f6d7a874/cogs/meta.py#L21). 

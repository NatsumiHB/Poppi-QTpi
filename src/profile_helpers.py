from datetime import datetime

import aiohttp
from pyArango.theExceptions import DocumentNotFoundError

from api_helpers import APIUtils
from poppi_helpers import PoppiError


class ProfileHelpers:
    def __init__(self, profile_collection, store_item_collection, config):
        self.profiles = profile_collection
        self.store_items = store_item_collection

        self.config = config

        # Used for image validation
        self.client_session = aiohttp.ClientSession()

    def get_or_create_profile(self, member_id: int, create_on_not_found: bool = False):
        try:
            profile = self.profiles[member_id]
        except DocumentNotFoundError:
            if create_on_not_found:
                profile = self.profiles.createDocument()
                profile._key = str(member_id)

                profile.set(self.config.empty_profile)

                profile.save()
            else:
                profile = self.config.empty_profile

        return profile

    async def set_profile_key(self, member_id: int, key: str, value):
        profile = self.get_or_create_profile(member_id, create_on_not_found=True)

        profile[key] = value

        human_key = key.replace('_', ' ').capitalize()

        max_length = self.config.profile_restraints[f"max_{key}_length"]

        if profile.validate() is False:
            raise PoppiError(f"Error validating {human_key}")

        if key == "avatar_url":
            await self.validate_avatar(value)

        if 0 < max_length < len(value):
            raise PoppiError(f"{human_key} can't be longer than {max_length}")
        else:
            profile.patch()

    def add_money(self, member_id: int, amount: int):
        profile = self.get_or_create_profile(member_id, create_on_not_found=True)

        profile["money"] += amount
        profile.patch()

    def subtract_money(self, member_id: int, amount: int):
        profile = self.get_or_create_profile(member_id, create_on_not_found=True)

        if profile["money"] < amount:
            raise PoppiError(f"You don't have enough {self.config.money_config['currency']} to do that")
        else:
            profile["money"] -= amount
            profile.patch()

    def transact_money(self, sender_id: int, recipient_id: int, amount: int):
        self.subtract_money(sender_id, amount)
        self.add_money(recipient_id, amount)

    def redeem_daily(self, member_id: int):
        profile = self.get_or_create_profile(member_id, create_on_not_found=False)

        if profile.last_daily is not None \
                and abs((datetime.utcnow() - datetime.strptime(profile.last_daily, "%Y-%m-%d %H:%M:%S.%f")).days) < 1:
            raise PoppiError(f"You already redeemed your daily {self.config.money_config['currency']} in the last 24h")

        self.add_money(member_id, self.config.money_config["daily_money"])

        profile["last_daily"] = datetime.utcnow()
        profile.patch()

    def get_item_by_id(self, item_id: int):
        for item in self.store_items.fetchAll():
            if item["id"] == item_id:
                return item

        raise PoppiError("That item couldn't be found")

    def check_inventory_for_item(self, member_id: int, item_id: int):
        profile = self.get_or_create_profile(member_id, create_on_not_found=True)

        return len(
            [inventory_item_id
             for inventory_item_id
             in profile["inventory"]
             if inventory_item_id == item_id]
        )

    def buy_item(self, member_id: int, item: dict):
        profile = self.get_or_create_profile(member_id, create_on_not_found=True)

        if self.check_inventory_for_item(member_id, item["id"]) >= item["max_amount"]:
            raise PoppiError(f"You can't have more than {item['max_amount']} of this item")

        self.subtract_money(member_id, item["price"])

        profile["inventory"].append(item["id"])
        profile.patch()

    async def validate_avatar(self, url: str):
        async with self.client_session.get(url) as r:
            if APIUtils.check_success(r.status) is False:
                raise PoppiError("Server returned non-2XX status code")

            if r.headers.get("content-type").startswith("image") is False:
                raise PoppiError("URL provided is not an image")

    async def is_valid_avatar(self, url: str):
        try:
            await self.validate_avatar(url)
            return True
        except PoppiError:
            return False

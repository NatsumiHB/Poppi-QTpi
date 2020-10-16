import aiohttp
from pyArango.theExceptions import DocumentNotFoundError

from api_utils import APIUtils
from poppi_helpers import PoppiError


class ProfileHelpers:
    def __init__(self, profile_collection, config):
        self.profiles = profile_collection

        self.empty_profile = config["empty_profile"]
        self.profile_restraints = config["profile_restraints"]

        # Used for image validation
        self.client_session = aiohttp.ClientSession()

    def get_or_create_profile(self, member_id: int, create_on_not_found: bool = False):
        try:
            profile = self.profiles[member_id]
        except DocumentNotFoundError:
            if create_on_not_found:
                profile = self.profiles.createDocument()
                profile._key = str(member_id)

                profile.set(self.empty_profile)

                profile.save()
            else:
                profile = self.empty_profile

        return profile

    async def set_profile_key(self, member_id: int, key: str, value):
        profile = self.get_or_create_profile(member_id, create_on_not_found=True)

        profile[key] = value

        human_key = key.replace('_', ' ').capitalize()

        max_length = self.profile_restraints[f"max_{key}_length"]

        if profile.validate() is False:
            raise PoppiError(f"Error validating {human_key}")

        if key == "avatar_url":
            await self.validate_avatar(value)

        if 0 < max_length < len(value):
            raise PoppiError(f"{human_key} can't be longer than {max_length}")
        else:
            profile.save()

    def add_money(self, member_id: int, amount: int):
        profile = self.get_or_create_profile(member_id, create_on_not_found=True)

        profile["money"] += amount

        profile.save()

    def subtract_money(self, member_id: int, amount: int):
        profile = self.get_or_create_profile(member_id, create_on_not_found=True)

        if profile["money"] < amount:
            raise PoppiError(f"You don't have enough money to do that")
        else:
            profile["money"] -= amount
            profile.save()

    def transact_money(self, sender_id: int, recipient_id: int, amount: int):
        self.subtract_money(sender_id, amount)
        self.add_money(recipient_id, amount)

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

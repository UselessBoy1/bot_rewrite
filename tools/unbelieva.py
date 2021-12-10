import asyncio
import aiohttp
from typing import Union, List, Optional


class RateLimit:
    """A representation of a rate limit. Allows for access to rate limit info."""

    def __init__(self, limit: int, remaining: int, reset):
        self.limit = limit
        self.remaining = remaining
        self.reset = reset


class Guild:
    """A representation of a Discord guild. Can be replaced by discord.py Guild."""

    def __init__(self, guild_id: int):
        """Initializes a Guild object with the specified id."""
        self.id = guild_id


class User:
    """\
    A representation of a Discord user. Can be replaced by discord.py User, but
    functions will still return an Pybelieva User."""

    def __init__(self, user_id: int, rank: Optional[int] = None, cash: int = 0,
                 bank: int = 0, total: int = 0, found: bool = True):
        """\
        Initializes an User object with the specified user_id, (optional) rank,
        cash, bank and total balance and found flag. Usage of any arguments
        except user_id is discouraged, as it traps the programmer into thinking
        that the values have been changed."""
        self.id = user_id
        self.rank = rank
        self.cash = cash
        self.bank = bank
        self.total = total


class Client:
    """An UnbelivaBoat API client. The heart of the Pybelieva."""

    def __init__(self, token: str, loop=None, base_url='https://unbelievable.pizza/api',
                 version=1):
        """\
        Initializes the Client with the specified token."""
        self._loop = loop or asyncio.get_event_loop()
        self._url = base_url
        self._version = version
        self._session = aiohttp.ClientSession(
            headers={'Authorization': token}, loop=self._loop, timeout=5)
        self.rate_limit = None

    def __del__(self):
        return self._loop.create_task(self._session.close())

    async def __request(self, retry, args, method, sub_url, json={}):
        """An internal function."""
        #  Sends a request and processes the response.
        request = await self._session.request(
            method, f'{self._url}/v{self._version}/guilds/{sub_url}', json=json)
        self.rate_limit = RateLimit(request.headers['X-RateLimit-Limit'],
                                    request.headers['X-RateLimit-Remaining'],
                                    request.headers['X-RateLimit-Reset'])

        body = await request.json()
        if type(body) is dict:
            if 'error' in body:
                raise ConnectionError(body['error'])
            if 'retry_after' in body:
                print(f'Sleep {body["retry_after"] / 1000} seconds')
                await asyncio.sleep(body['retry_after'] / 1000)
                print('Ended sleeping')
                return await retry(*args)
            return User(**body)
        return [User(**user) for user in body]

    async def get_balance(self, guild: Guild, user:
    User) -> User:
        """\
        GET User Balance as described by API Documentation. Queries user's
        balance.

        Returns a User with the updated balance."""
        return await self.__request(self.get_balance, [guild, user], 'GET',
                                    f'{guild.id}/users/{user.id}')

    async def get_leaderboard(self, guild: Guild) -> List[User]:
        """\
        GET Guild Leaderboard as described by API Documentation. Queries all
        user's balances in a guild.

        Returns a User list with the actual balance, ordered by rank."""
        return await self.__request(self.get_leaderboard, [guild],
                                    'GET', f'{guild.id}/users')

    async def edit_balance(self,
                           guild: Guild, user: User,
                           cash: int = 0, bank: int = 0,
                           reason: Optional[str] = None) -> User:
        """\
        PATCH User Balance as described by API Documentation. Adds money to
        user's cash and bank accordingly.

        Returns a User with the updated balance."""
        return await self.__request(self.edit_balance, [guild, user, cash, bank],
                                    'PATCH', f'{guild.id}/users/{user.id}',
                                    json={
                                        'cash': cash,
                                        'bank': bank,
                                        'reason': reason,
                                    })

    async def set_balance(self, guild: Guild, user:
    User, cash: int = 0, bank: int = 0,
                          reason: Optional[str] = None) -> User:
        """\
        PUT User Balance as described by API Documentation. Sets user's cash and
        bank balance to the specified values.

        Returns a User with the updated balance."""
        return await self.__request(self.set_balance, [guild, user, cash, bank],
                                    'PUT', f'{guild.id}/users/{user.id}',
                                    json={
                                        'cash': cash,
                                        'bank': bank
                                    })

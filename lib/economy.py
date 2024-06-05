# Load Cogs
import json
from discord.ext import commands


async def get_bank_data():
    with open('../bank.json', 'r') as f:
        users = json.load(f)
    return users


async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:  # Crete all the different banks, wallets and ect if user doesn't have one already
        users[str(user.id)] = {}
        users[str(user.id)]["Wallet"] = 0  # User wallet
        users[str(user.id)]["Bank"] = 0  # User bank
        users[str(user.id)]["Wins"] = 0  # User amounts of wins
        users[str(user.id)]["Earned"] = 0  # User total amount coins earned (In lifetime)
        users[str(user.id)]["Losses"] = 0  # User amounts of losses
        users[str(user.id)]["Lost"] = 0  # User total amount of coins lost (In lifetime)
        users["GEarned"] = 0  # Global total amount of coins lost (In lifetime)
        users["GLost"] = 0  # Global total amount of coins lost (In lifetime)
        users["GWins"] = 0  # Global amounts of wins (In lifetime)

    with open("./bank.json", 'w') as f:
        json.dump(users, f)

    return True


async def update_bank(user, change=0, mode="Wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("./bank.json", 'w') as f:
        json.dump(users, f)
    bal = [users[str(user.id)]["Wallet"], users[str(user.id)]["Bank"], users[str(user.id)]["Wins"],
           users[str(user.id)]["Earned"], users[str(user.id)]["Losses"], users[str(user.id)]["Lost"]]
    return bal


class Economy(commands.Cog):
    """
    Managing economy related commands
    """
    def __init__(self, bot):
        self.bot = bot

    # Your economy related commands and methods go here


async def setup(bot):
    await bot.add_cog(Economy(bot))

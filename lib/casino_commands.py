import asyncio
import datetime
import json
import random
from datetime import datetime
from inspect import currentframe, getframeinfo
import discord
import discord.utils
from discord.ext import commands
from . import economy
from .economy import open_account, get_bank_data, update_bank

"""MONEY SYSTEM"""
""""Bank"""


class Casino(commands.Cog):
    """
    Gamble your money, and see if you can win big or lose it all.
    """

    def init(self, Bot):
        pass

    @commands.command(aliases=['stat'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def stats(self, ctx):
        print(
            f'{datetime.now()}: {ctx.message.author} executed command - {[str(ctx.guild.id)]}{ctx.invoked_with}')

        await economy.open_account(ctx.author)
        user = ctx.author
        users = await economy.get_bank_data()

        wins_atm = users[str(user.id)]["Wins"]
        total_coins_earned_amt = users[str(user.id)]["Earned"]
        losses_amt = users[str(user.id)]["Losses"]
        total_coins_lost_amt = users[str(user.id)]["Lost"]
        global_earned = users["GEarned"]
        global_losts = users["GLost"]

        em = discord.Embed(title=f"{ctx.author.name}'s statistics", color=discord.Color.teal())
        em.add_field(name="Total wins:", value=wins_atm)
        em.add_field(name="Total coins earned:", value=total_coins_earned_amt)
        em.add_field(name="**-**", value="**-**", inline=False)
        em.add_field(name="Total losses:", value=losses_amt)
        em.add_field(name="Total coins lost:", value=total_coins_lost_amt)
        em.add_field(name="--------------------------------------------------", value="\n**Global Statistics**",
                     inline=False)
        em.add_field(name="Global earned coins", value=global_earned)
        em.add_field(name="Global coins lost", value=global_losts)
        await ctx.send(embed=em)

    @commands.command(aliases=['bal'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def balance(self, ctx):
        print(
            f'{datetime.now()}: {ctx.message.author} executed command - {[str(ctx.guild.id)]}{ctx.invoked_with}')

        await economy.open_account(ctx.author)

        user = ctx.author

        users = await economy.get_bank_data()

        wallet_amt = users[str(user.id)]["Wallet"]
        bank_amt = users[str(user.id)]["Bank"]

        em = discord.Embed(title=f"{ctx.author.name}'s balance.", color=discord.Color.teal())
        em.add_field(name="Wallet Balance", value=wallet_amt)
        em.add_field(name="Bank Balance", value=bank_amt)
        await ctx.send(embed=em)

    @commands.command(aliases=['ch'])
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def chest(self, ctx):
        print(
            f'{datetime.now()}: {ctx.message.author} executed command - {[str(ctx.guild.id)]}{ctx.invoked_with}')

        await economy.open_account(ctx.author)

        user = ctx.author

        users = await economy.get_bank_data()

        earnings = random.randrange(3001)

        await ctx.send(f"The chest had ``{earnings}``$ in it, congrats!")

        users[str(user.id)]["Wallet"] += earnings

        with open("../bank.json", 'w') as f:
            json.dump(users, f)

    @chest.error
    async def chest_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                'You have already opened the chest today, you have to wait {:.2f}h'.format(error.retry_after / 60 / 60))

    @commands.command(aliases=['wit'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def withdraw(self, ctx, amount=None):
        print(
            f'{datetime.now()}: {ctx.message.author} executed command - {[str(ctx.guild.id)]}{ctx.invoked_with}')

        await economy.open_account(ctx.author)

        if amount is None:
            await ctx.send("Please enter the amount")
            return

        bal = await economy.update_bank(ctx.author)

        amount = int(amount)
        if amount > bal[1]:
            await ctx.send("You don't have that amount of money!")
            return
        if amount < 0:
            await ctx.send("Amount must be positive!")
            return

        await economy.update_bank(ctx.author, amount)
        await economy.update_bank(ctx.author, -1 * amount, "Bank")

        await ctx.send(f"You withdrew {amount}$!")

    @commands.command(aliases=['dep'])
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def deposit(self, ctx, amount=None):
        print(
            f'{datetime.now()}: {ctx.message.author} executed command - {[str(ctx.guild.id)]}{ctx.invoked_with}')

        await economy.open_account(ctx.author)

        if amount is None:
            await ctx.send("Please enter the amount")
            return

        bal = await economy.update_bank(ctx.author)

        amount = int(amount)
        if amount > bal[0]:
            await ctx.send("You don't have that amount of money!")
            return
        if amount < 0:
            await ctx.send("Amount must be positive!")
            return

        await economy.update_bank(ctx.author, -1 * amount)
        await economy.update_bank(ctx.author, amount, "Bank")

        await ctx.send(f"You deposited {amount}$!")

    """Gamble"""

    # Gamble
    @commands.command()
    @commands.cooldown(rate=1, per=2)
    async def dice(self, ctx, nr: int = None, bet: int = None):
        print(
            f'{datetime.now()}: {ctx.message.author} executed command - {[str(ctx.guild.id)]}{ctx.invoked_with}')

        user = ctx.author
        users = await economy.get_bank_data()
        n = random.randrange(1, 6)  # Where does it bot_starter and end
        # Errors
        error = discord.Embed(title=f"Dice_Error {getframeinfo(currentframe()).lineno}",
                              description="You must pick a number between 1 and 6", color=discord.Color.orange())
        high_error = discord.Embed(title=f"Dice_Error {getframeinfo(currentframe()).lineno}",
                                   description="The number is too high, it must be between 1 and 6",
                                   color=discord.Color.orange())
        low_error = discord.Embed(title=f" Dice_Error {getframeinfo(currentframe()).lineno}",
                                  description="You must pick a number between 1 and 6", color=discord.Color.orange())
        # Bet Errors
        bet_none_error = discord.Embed(title=f"Bet_Error {getframeinfo(currentframe()).lineno}",
                                       description="You must place a bet", color=discord.Color.orange())
        low_bet_error = discord.Embed(title=f"Bet_Error {getframeinfo(currentframe()).lineno}",
                                      description="The lowest amount you can bet is 10 coins, try to bet 10 coins or more",
                                      color=discord.Color.orange())
        high_bet_error = discord.Embed(title=f"Bet_Error {getframeinfo(currentframe()).lineno}",
                                       description="Sorry, you can't bet more than 10000 coins",
                                       color=discord.Color.orange())
        poor_bet_error = discord.Embed(title=f"Bet_Error {getframeinfo(currentframe()).lineno}",
                                       description="You don't have that much money in your wallet. Fun fact, u are poor",
                                       color=discord.Color.orange())

        # Sending confirmation embed
        message = discord.Embed(title=f"You betet {bet} coins on {nr}, let's see if you win!\n Dice: ❔",
                                color=discord.Color.light_gray())
        message0 = discord.Embed(title=f"You betet {bet} coins on {nr}, let's see if you win!\n Dice: **{n}** ",
                                 color=discord.Color.light_gray())
        # Win or lost
        lost = discord.Embed(title=f"Seems like you lost, the dice landed on {n} and u lost your bet on {bet} coins",
                             color=discord.Color.red())

        if nr is None:  # You didn't pick a number
            await ctx.send(embed=error)
        elif nr > 6:  # Your number is too high
            await ctx.send(embed=high_error)
        elif nr < 1:  # Your number is too low
            await ctx.send(embed=low_error)
        else:
            # Controls the betting is right
            if bet is None:
                await ctx.send(embed=bet_none_error)
            elif bet < 10:
                await ctx.send(embed=low_bet_error)
            elif bet > 10000:
                await ctx.send(embed=high_bet_error)
            elif bet > users[str(user.id)]["Wallet"]:
                await ctx.send(embed=poor_bet_error)

            else:
                print("Made it trough all fail-safes")
                msg_send = await ctx.send(embed=message, delete_after=10)
                await asyncio.sleep(4)
                await msg_send.edit(embed=message0)
                print("Double check is done")

                if n == nr:  # You won, you guessed the same number as the dice got
                    win = discord.Embed(title=f"CONGRATS\n The dice landed on {n} and u won {bet * 3} coins!!!",
                                        color=discord.Color.green())
                    await economy.open_account(ctx.author)

                    await ctx.send(embed=win)

                    users[str(user.id)]["Wallet"] += bet * 2

                    with open("../bank.json", 'w') as f:

                        json.dump(users, f)
                elif n is not nr:  # You lost, you did not guess the right number.
                    user = ctx.author
                    users = await economy.get_bank_data()
                    print("User lost the Dice game")

                    users[str(user.id)]["Wallet"] -= bet
                    users[str(user.id)]["Losses"] += 1
                    users[str(user.id)]["Lost"] -= bet
                    users["GLost"] -= bet

                    with open("../bank.json", 'w') as f:

                        json.dump(users, f)

                    await ctx.send(embed=lost)

    # Dice errors
    @dice.error
    async def dice_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            errormsg = (
                [
                    discord.Embed(title="CALM DOWN, THERE IS A COOLDOWN",
                                  description=f'Jeez try again in {error.retry_after:2f}s.',
                                  color=discord.Color.orange()),
                    discord.Embed(title="Duuude, wait a bit",
                                  description=f'{error.retry_after:2f}s left until you can use the command again',
                                  color=discord.Color.orange()),
                    discord.Embed(title="BREATH, BREATH, BREATH}",
                                  description=f'there is a cooldown and it is {error.retry_after:2f}s left',
                                  color=discord.Color.orange()),
                    discord.Embed(title=f"{error.retry_after:2f}s left",
                                  description=f'{error.retry_after:2f}s left, {error.retry_after:2f}s left, {error.retry_after:2f}s left, {error.retry_after:2f}s left, {error.retry_after:2f}s left, {error.retry_after:2f}s left, {error.retry_after:2f}s left, {error.retry_after:2f}s left',
                                  color=discord.Color.orange()),
                    discord.Embed(title="Gamble addicted?",
                                  description=f'Sooo you are one of those called "gamble addicted"? Wait {error.retry_after:2f}s',
                                  color=discord.Color.orange()),
                    discord.Embed(title="Rush?",
                                  description=f'Are you in a rush my friend? {error.retry_after:2f}s. Rush B next time friendo',
                                  color=discord.Color.orange()),
                    discord.Embed(title="I have a msg for Phy",
                                  description=f'We should delete the cooldown so people can get poor faster than ever before, btw {error.retry_after:2f}s left until you can lose more money',
                                  color=discord.Color.orange())
                ]
            )
            await ctx.send(embed=random.choice(errormsg), delete_after=7)

    """fixed the this shit"""

    @commands.command()
    @commands.cooldown(rate=1, per=4)
    async def slot(self, ctx, bet: int = None):
        print(
            f'{datetime.now()}: {ctx.message.author} executed command - {[str(ctx.guild.id)]}{ctx.invoked_with}')

        # Variables & def
        user = ctx.author
        users = await economy.get_bank_data()
        slots1 = (
            [
                "🟢",  # Green
                "💛",  # Yellow
                "🔷",  # Blue
                "🖤",  # Black
                "❤",  # Red
                "🟣"  # Purple
            ]
        )
        slots2 = (
            [
                "🟢",  # Green
                "💛",  # Yellow
                "🔷",  # Blue
                "🖤",  # Black
                "❤",  # Red
                "🟣"  # Purple
            ]
        )
        slots3 = (
            [
                "🟢",  # Green
                "💛",  # Yellow
                "🔷",  # Blue
                "🖤",  # Black
                "❤",  # Red
                "🟣"  # Purple
            ]
        )
        S1 = random.choice(slots1)
        S2 = random.choice(slots2)
        S3 = random.choice(slots3)

        usd = "💲💲💲"

        async def message():
            slotbed = discord.Embed(title=f"Slot Machine: You beted {bet}, lets see if you win",
                                    description=f"❔ ❔ ❔", color=discord.Color.light_gray())
            slotbedS1 = discord.Embed(title=f"Slot Machine: You beted {bet}, lets see if you win",
                                      description=f"{S1} ❔ ❔", color=discord.Color.light_gray())
            slotbedS2 = discord.Embed(title=f"Slot Machine: You beted {bet}, lets see if you win",
                                      description=f"{S1} {S2} ❔", color=discord.Color.light_gray())
            slotbedS3 = discord.Embed(title=f"Slot Machine: You beted {bet}, lets see if you win",
                                      description=f"{S1} {S2} {S3}", color=discord.Color.light_gray())
            global message
            message = await ctx.send(embed=slotbed)

            await asyncio.sleep(1)
            await message.edit(embed=slotbedS1)
            await asyncio.sleep(1)
            await message.edit(embed=slotbedS2)
            await asyncio.sleep(1)
            await message.edit(embed=slotbedS3)

        async def lose():  # Lose message
            global message
            slotlose = discord.Embed(title=f"Sorry, you just lost {bet} coins",
                                     description=f"{S1, S2, S3}", color=discord.Color.red())
            await message.edit(embed=slotlose)
            print(
                f'S3 = False \n {ctx.author} beted {bet} and lost it all \n Wallet Before: {users[str(user.id)]["Wallet"]}'
                f' \n Current Wallet:{users[str(user.id)]["Wallet"] - bet} test \n ----------------')

            users[str(user.id)]["Wallet"] -= bet
            users[str(user.id)]["Losses"] += 1
            users[str(user.id)]["Lost"] -= bet
            users["GLost"] -= bet

        async def win():  # Win message
            global message
            slotwon = discord.Embed(title=f"Congrats!!! You just won {bet * 10} coins",
                                    description=f"{S1, S2, S3}", color=discord.Color.green())

            print(
                f"""S3 = True \n {ctx.author} beted {bet} and won {bet * 10} \n Wallet Before: {users[str(user.id)]["Wallet"]}
                 \n Now has:{users[str(user.id)]["Wallet"] + bet * 10} test \n ----------------""")

            await message.edit(embed=slotwon)

            users[str(user.id)]["Wallet"] += bet * 5
            users[str(user.id)]["Wins"] += 1
            users[str(user.id)]["Earned"] += bet * 5
            users["GEarned"] += bet * 5

        async def jackpot():  # Jackpot message
            global message
            slotjackpot = discord.Embed(title=f"CONGRATS, YOU WON THE JACKPOT {bet * 1000} {usd}",
                                        description=f"{S1, S2, S3}", color=discord.Color.dark_green())
            print(
                f'S3 = True \n {ctx.author} beted {bet} and won {bet * 10} \n Wallet Before: {users[str(user.id)]["Wallet"]}'
                f' \n Now has:{users[str(user.id)]["Wallet"] + bet * 10} test \n ----------------')
            await message.edit(embed=slotjackpot)
            users[str(user.id)]["Wallet"] += bet * 500
            users[str(user.id)]["Wins"] += 1
            users[str(user.id)]["Earned"] += bet * 500
            users["GEarned"] += bet * 500

        # Code
        if bet is None:  # Checks if user didn't forget to place a bet amount
            error_slot = discord.Embed(title=f"ERROR!",
                                       description=f"You must place a bet! The lowest amount of coins you can bet is 100 or highest is 100,000.",
                                       color=discord.Color.orange())
            return await ctx.send(embed=error_slot)

        if bet < 100:  # Checks if user don't bet less than 100 points
            error_slot = discord.Embed(title=f"ERROR!",
                                       description=f"You can't bet {bet}!!! The bet must be 100 coins or more!",
                                       color=discord.Color.orange())
            return await ctx.send(embed=error_slot)

        if bet > 100000:  # Checks if user don't bet more than 100 000
            error_slot = discord.Embed(title=f"ERROR!",
                                       description=f"You can't bet {bet}!!! The highest amount of coins you can bet is 100,000!",
                                       color=discord.Color.orange())
            return await ctx.send(embed=error_slot)

        if bet > users[str(user.id)]["Wallet"]:  # Checks if user is betting more than what exists in their wallet
            error_slot = discord.Embed(title=f"Bank Error!",
                                       description=f"You don't have that much coins in your wallet, check your bank!!",
                                       color=discord.Color.orange())
            return await ctx.send(embed=error_slot)

        else:
            await message()

            if S1 == S2 == S3:  # Win jackpot if you get 3 red hearts
                await jackpot()  # Wins 1000x times what you bet

            elif all(symbol in ["💛", "🖤", "❤"] for symbol in (S1, S2, S3)):  # Checks for 3 hearts, color doesn't matter
                await win()  # Wins 10x times what you bet
            else:
                await lose()  # Lose, you lose all the money you bet

        with open("../bank.json"
                  "", 'w') as f:  # Gives you the new value in your wallet
            json.dump(users, f)
        return

    @commands.command()
    @commands.cooldown(rate=1, per=4)
    async def blackjack(self, ctx, bet: int = None):
        print(
            f'{datetime.now()}: {ctx.message.author} executed command - {[str(ctx.guild.id)]}{ctx.invoked_with}')

        # Variables
        user = ctx.author
        users = await economy.get_bank_data()
        cards = {
            "🂡": 1,
            "🂢": 2,
            "🂣": 3,
            "🂤": 4,
            "🂥": 5,
            "🂦": 6,
            "🂧": 7,
            "🂨": 8,
            "🂩": 9,
            "🂪": 10,
            "🂫": 10,
            "🂭": 10,
            "🂮": 10,
            "🂱": 1,
            "🂲": 2,
            "🂳": 3,
            "🂴": 4,
            "🂵": 5,
            "🂶": 6,
            "🂷": 7,
            "🂸": 8,
            "🂹": 9,
            "🂺": 10,
            "🂻": 10,
            "🂽": 10,
            "🂾": 10,
            "🃁": 1,
            "🃂": 2,
            "🃃": 3,
            "🃄": 4,
            "🃅": 5,
            "🃆": 6,
            "🃇": 7,
            "🃈": 8,
            "🃉": 9,
            "🃊": 10,
            "🃋": 10,
            "🃍": 10,
            "🃎": 10,
            "🃑": 1,
            "🃒": 2,
            "🃓": 3,
            "🃔": 4,
            "🃕": 5,
            "🃖": 6,
            "🃗": 7,
            "🃘": 8,
            "🃙": 9,
            "🃚": 10,
            "🃛": 10}
        cards_list = list(cards.keys())
        dealer_cards = []
        player_cards = []
        dealer_sum = 0
        player_sum = 0

        random.choice(cards_list)



async def setup(bot):
    await bot.add_cog(Casino(bot))

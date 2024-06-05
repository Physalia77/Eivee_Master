import random

# Bot status
"""
total_members_count = len(bot.users)

status = [f"Member count: {total_members_count}", "Defualt help command: ?help",
          f"{self.bot.user.name} is in {len(bot.guilds)} servers!"]


async def change_status():
    await bot.wait.until_ready
    msgs = cycle(status)

    while not bot.is_bot:
        current_status = next(msgs)
        await bot.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep()
"""

import os
import stat

"""MAKE FILE READABLE"""

"""
def make_file_readable(filepath):
    # Add read permission to the current file's permissions
    os.chmod(filepath, os.stat(filepath).st_mode | stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)


# Usage
filepath = '../lib/economy.py'
make_file_readable(filepath)
"""
"""IS FILE READABLE"""

"""


def is_file_readable(filepath):
    return os.access(filepath, os.R_OK)


# Usage
filepath = '../lib/economy.py'
if is_file_readable(filepath):
    print(f"The file '{filepath}' is readable.")
else:
    print(f"The file '{filepath}' is not readable.")

with open('../logs/log.log', 'w'):
    pass
"""

# Variables
cards = {
    "🂡": {"name": "Ace of Spades", "value": 1},
    "🂢": {"name": "Two of Spades", "value": 2},
    "🂣": {"name": "Three of Spades", "value": 3},
    "🂤": {"name": "Four of Spades", "value": 4},
    "🂥": {"name": "Five of Spades", "value": 5},
    "🂦": {"name": "Six of Spades", "value": 6},
    "🂧": {"name": "Seven of Spades", "value": 7},
    "🂨": {"name": "Eight of Spades", "value": 8},
    "🂩": {"name": "Nine of Spades", "value": 9},
    "🂪": {"name": "Ten of Spades", "value": 10},
    "🂫": {"name": "Jack of Spades", "value": 10},
    "🂭": {"name": "Queen of Spades", "value": 10},
    "🂮": {"name": "King of Spades", "value": 10},
    "🂱": {"name": "Ace of Hearts", "value": 1},
    "🂲": {"name": "Two of Hearts", "value": 2},
    "🂳": {"name": "Three of Hearts", "value": 3},
    "🂴": {"name": "Four of Hearts", "value": 4},
    "🂵": {"name": "Five of Hearts", "value": 5},
    "🂶": {"name": "Six of Hearts", "value": 6},
    "🂷": {"name": "Seven of Hearts", "value": 7},
    "🂸": {"name": "Eight of Hearts", "value": 8},
    "🂹": {"name": "Nine of Hearts", "value": 9},
    "🂺": {"name": "Ten of Hearts", "value": 10},
    "🂻": {"name": "Jack of Hearts", "value": 10},
    "🂽": {"name": "Queen of Hearts", "value": 10},
    "🂾": {"name": "King of Hearts", "value": 10},
    "🃁": {"name": "Ace of Diamonds", "value": 1},
    "🃂": {"name": "Two of Diamonds", "value": 2},
    "🃃": {"name": "Three of Diamonds", "value": 3},
    "🃄": {"name": "Four of Diamonds", "value": 4},
    "🃅": {"name": "Five of Diamonds", "value": 5},
    "🃆": {"name": "Six of Diamonds", "value": 6},
    "🃇": {"name": "Seven of Diamonds", "value": 7},
    "🃈": {"name": "Eight of Diamonds", "value": 8},
    "🃉": {"name": "Nine of Diamonds", "value": 9},
    "🃊": {"name": "Ten of Diamonds", "value": 10},
    "🃋": {"name": "Jack of Diamonds", "value": 10},
    "🃍": {"name": "Queen of Diamonds", "value": 10},
    "🃎": {"name": "King of Diamonds", "value": 10},
    "🃑": {"name": "Ace of Clubs", "value": 1},
    "🃒": {"name": "Two of Clubs", "value": 2},
    "🃓": {"name": "Three of Clubs", "value": 3},
    "🃔": {"name": "Four of Clubs", "value": 4},
    "🃕": {"name": "Five of Clubs", "value": 5},
    "🃖": {"name": "Six of Clubs", "value": 6},
    "🃗": {"name": "Seven of Clubs", "value": 7},
    "🃘": {"name": "Eight of Clubs", "value": 8},
    "🃙": {"name": "Nine of Clubs", "value": 9},
    "🃚": {"name": "Ten of Clubs", "value": 10},
    "🃛": {"name": "Jack of Clubs", "value": 10},
    "🃝": {"name": "Queen of Clubs", "value": 10},
    "🃞": {"name": "King of Clubs", "value": 10},
}
dealer_cards = []
player_cards = []
dealer_sum = 0
player_sum = 0

# Select a random card for player
print("\nPLAYER:")
for _ in range(2):
    selected_card = random.choice(list(cards.keys()))
    print(f"Card: {selected_card}, Name: {cards[selected_card]['name']}, Value: {cards[selected_card]['value']}")
    player_cards.append(selected_card)

def player_hit(player_sum, player_cards):
    # Select a random card for player
    print("\nPLAYER:")
    selected_card = random.choice(list(cards.keys()))
    print(f"Card: {selected_card}, Name: {cards[selected_card]['name']}, Value: {cards[selected_card]['value']}")
    player_cards.append(selected_card)
    player_sum += cards[selected_card]['value']  # Add the value of the new card to the player's sum
    print(f"Player sum: {player_sum}")
    return player_sum  # Return the updated player_sum


# Select a random card for dealer
print("\nDEALER:")
selected_card = random.choice(list(cards.keys()))
print(f"Card: {selected_card}, Name: {cards[selected_card]['name']}, Value: {cards[selected_card]['value']}")
dealer_cards.append(selected_card)
# Select a second card for dealer but don't reveal it
selected_card = random.choice(list(cards.keys()))
dealer_cards.append(selected_card)
dealer_sum += cards[selected_card]['value']  # Add the value of the hidden card to the dealer's sum


def hit_stand_double(player_sum, player_cards, dealer_sum, dealer_cards):
    select = input("\nDo you want to hit, stand or double? [Hit] [Stand] [Double]\n")

    if select.lower() == "hit":
        player_sum = player_hit(player_sum, player_cards)  # Update player_sum with the returned value
        if player_sum > 21:
            print("Player busts!")
        else:
            hit_stand_double(player_sum, player_cards, dealer_sum, dealer_cards)
    if select.lower() == "stand":
        print("Player stands!")

    if select.lower() == "double":
        print("Player doubles!")

    if select.lower() == "ch dealer":
        for card in dealer_cards:
            print(f"Card: {card}, Name: {cards[card]['name']}, Value: {cards[card]['value']}")


hit_stand_double(player_sum, player_cards, dealer_sum, dealer_cards)

# Python Standard Library Imports
import os.path
from inspect import currentframe, getframeinfo
import logging
import asyncio

# Third-party imports
import discord
import discord.utils
import pyfiglet
from discord.ext import commands
from discord.ext.commands import bot
from termcolor import colored
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

"""LOG SYSTEM"""

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler
handler = logging.FileHandler('logs/log.log')
handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

"""REPORT SYSTEM"""
# Create a logger for reporting
report_logger = logging.getLogger('report')
report_logger.setLevel(logging.DEBUG)

# Create a file handler for the logger
handler = logging.FileHandler('logs/report.log')
handler.setLevel(logging.DEBUG)

# Create a logging format including the timestamp
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M')

# Set the formatter for the handler
handler.setFormatter(formatter)

# Add the handler to the logger
report_logger.addHandler(handler)

# Log a message indicating that the script has been restarted
report_logger.info("\n\nScript restarted")

# Constants
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
traceback = True

# Functions
# function for opening prefixes.json, but switching to sql


# Bot Initialization
bot = commands.Bot(command_prefix='?', case_insensitive=True, intents=discord.Intents.all())
bot.remove_command('help')

# Change directory to script path
os.chdir(DIR_PATH)

# Variables
initial_extensions = []


# Load Prefixes


# Bot Commands
@bot.command(name="check_cogs", aliases=["check cog", "cc"],
             descreption="Look if cog/extension is loaded or not.")
async def check_cogs(ctx, cog_name):
    try:
        await bot.load_extension(f"cogs.{cog_name}")
    except commands.ExtensionAlreadyLoaded:
        await ctx.send("Cog is loaded")
    except commands.ExtensionNotFound:
        await ctx.send("Cog not found")
    else:
        await ctx.send("Cog is unloaded")
        await bot.unload_extension(f"cogs.{cog_name}")


# Load cog/extension
@bot.command(name="load", description="Enable a specific extension")
async def load(ctx, extension=None):
    if extension is None:
        await ctx.send(
            embed=discord.Embed(title=f"Error: Arg extension missing [{getframeinfo(currentframe()).lineno}]",
                                description="You have to name an extension that you want to enable", color=0xF30000,
                                delete_after=7))
    else:
        try:
            await bot.load_extension(extension)
            print(f'loaded. {format(extension)}')
            logger.info(f'loaded. {format(extension)}, {ctx.author, ctx.guild.name, ctx.guild.id}')
            await ctx.send(embed=discord.Embed(title=f"Enabled `{format(extension)}`",
                                               description=f"Extension `{format(extension)} was successfully enabled",
                                               color=0xF30000, delete_after=7))
        except Exception as error:
            print(colored(f'{format(extension)} cannot be loaded. [{format(error)}]', 'red'))
            logger.info(
                f'{format(extension)} cannot be loaded. [{format(error)}], {ctx.author, ctx.guild.name, ctx.guild.id}')
            await ctx.send(embed=discord.Embed(title=f"Error: `{getframeinfo(currentframe()).lineno}`",
                                               description=f'{format(extension)} cannot be loaded. [{format(error)}]',
                                               color=0xF30000, delete_after=7))


# unLoad cog/extension
@bot.command(name="unload", description="Disable a specific extension")
async def unload(ctx, extension=None):
    if extension is None:
        await ctx.send(
            embed=discord.Embed(title=f"Error: Arg extension missing [{getframeinfo(currentframe()).lineno}]",
                                description="You have to name an extension that you want to disable", color=0xF30000,
                                delete_after=7))
    else:
        try:
            await bot.unload_extension(extension)
            print(f'Unloaded. {format(extension)}, {ctx.author, ctx.guild.name, ctx.guild.id} ')
            logger.info(f'Unloaded. {format(extension)}, {ctx.author, ctx.guild.name, ctx.guild.id} ')
            await ctx.send(embed=discord.Embed(title=f"Disabled `{format(extension)}`",
                                               description=f"Extension `{format(extension)} was successfully disabled",
                                               color=0xF30000, delete_after=7))
        except Exception as error:
            print(colored(f'{format(extension)} cannot be unloaded. [{format(error)}]', 'red'))
            logger.info(
                f'{format(extension)} cannot be unloaded. [{format(error)}], {ctx.author, ctx.guild.name, ctx.guild.id}')
            await ctx.send(embed=discord.Embed(title=f"Error: `{getframeinfo(currentframe()).lineno}`",
                                               description=f'{format(extension)} cannot be loaded. [{format(error)}]',
                                               color=0xF30000, delete_after=7))


# Python

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the 'lib' directory
lib_dir = os.path.join(current_dir, '..', 'lib')

# Load extensions from the 'lib' directory
for filename in os.listdir(lib_dir):
    if filename.endswith('.py'):
        initial_extensions.append(f'lib.{os.path.splitext(filename)[0]}')

# Load extensions from the current directory
for filename in os.listdir('./'):
    if filename.endswith('.py') and filename != "main.py":
        initial_extensions.append(os.path.splitext(filename)[0])


async def load_extensions(bot, extensions):
    for extension in extensions:
        if extension not in bot.extensions:  # Check if the extension is not already loaded
            try:
                await bot.load_extension(extension)
            except Exception as error:
                report_logger.error(f'Failed to load extension {extension}. \n{type(error).__name__}: {error}')

# Load extensions
loop = asyncio.get_event_loop()
loop.run_until_complete(load_extensions(bot, initial_extensions))


# Main Execution
@bot.event
async def on_ready():
    print(f'\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    print()

    ascii_banner = pyfiglet.figlet_format("EIVEE")
    print(colored(ascii_banner, "magenta"), end="")
    print()
    print(f'\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    print()
    print("Existing COGS:")
    nr = 0
    error_messages = []
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            nr += 1
            print(f"    COG #{nr} {format(extension)}")
        except commands.ExtensionAlreadyLoaded:
            nr += 1
            print(f"    COG #{nr} {format(extension)} is loaded.")
        except Exception as error:
            error_messages.append(f'    {format(extension)} cannot be loaded. [{format(error)}]')

    # Print error messages after all successful load attempts
    for error_message in error_messages:
        print(colored(error_message, 'red'))

    commands_list = [c.name for c in bot.commands]
    print(f'\nCommand List:', ', '.join(commands_list))

    await load_extensions(bot, initial_extensions)

    print(f'\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')

    def print_directory_structure(startpath, project_name):
        print(f'\n\n{project_name}/')
        for root, dirs, files in os.walk(startpath):
            # Skip certain directories
            if '.idea' in dirs:
                dirs.remove('.idea')
            if 'venv' in dirs:
                dirs.remove('venv')

            level = root.replace(startpath, '').count(os.sep)
            if level == 1:
                indent = '│' + ' ' * 4 * (level - 1) + '├── '
                print(f'{indent}{os.path.basename(root)}/')
                subindent = '│' + ' ' * 4 * level + '├── '
                for f in files:
                    print(f'{subindent}{f}')

    # Call the function with the path to your project root and the project name
    print_directory_structure('..', 'Project Root')


""
if __name__ == '__main__':
    """bot.loop.create0_task((change_status()))"""
    bot.run('')

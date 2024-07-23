import discord
from discord.ext import commands
import logging
import getpass
import sys


logging.basicConfig(level=logging.INFO)


def afficher_instructions():
    cadre = (
        "▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄\n"
        "█░▄▀█░▄▀▄░█░▄▄▀█░██░████░▄▄▀█░██░███░▄▄░█░██░▄▄▀█▀▄▀█▀▄▀█▀▄▄▀█░██░█░▄▄▀█▄░▄\n"
        "█░█░█░█▄█░█░▀▀░█░██░████░▄▄▀█░▀▀░█████▄▀█░██░▀▀░█░█▀█░█▀█░██░█░██░█░██░██░█\n"
        "█▄▄██▄███▄█▄██▄█▄▄█▄▄███▄▄▄▄█▀▀▀▄███░▀▀░█▄▄█▄██▄██▄███▄███▄▄███▄▄▄█▄██▄██▄█\n"
        "▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀\n"
    )
    instructions = (
        "Le token est invisible pour sécurité. Une fois copié, appuyez sur Entrée.\n"
        "Veuillez entrer le token de votre bot: "
    )
    print(cadre)
    print(instructions, end='')


def obtenir_token():
    afficher_instructions()
    return getpass.getpass()


TOKEN = obtenir_token()

if not TOKEN:
    logging.error('Le token du bot est incorrect ou non défini.')
    sys.exit(1)


intents = discord.Intents.default()
intents.message_content = True
intents.members = True  

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logging.info(f'Bot connecté en tant que {bot.user}')
    print("\nLe bot est prêt et connecté.")
    print("Commande = !msg message nombre")

@bot.command(name='msg')
async def msg(ctx, message: str, repeat: int):
    logging.info(f'Commande msg reçue avec le message: {message} à répéter {repeat} fois')
    count = 0
    for member in ctx.guild.members:
        if member != bot.user:
            try:
                for _ in range(repeat):
                    await member.send(message)
                logging.info(f'{repeat} messages envoyés à {member.name}')
                count += 1
            except Exception as e:
                logging.error(f'Impossible d\'envoyer le message à {member.name}: {e}')
    await ctx.send(f'{count} membres ont reçu le message.')


try:
    bot.run(TOKEN)
except discord.errors.LoginFailure as e:
    logging.error(f'Erreur de connexion : {e}')
except Exception as e:
    logging.error(f'Erreur inattendue: {e}')

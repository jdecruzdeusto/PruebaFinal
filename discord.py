import discord
from discord.ext import commands
import pandas as pd
from discord_webhook import DiscordWebhook

# Configura tu bot
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Suponemos que 'encoder', 'model', 'categorical_columns' y 'features' ya están definidos

@bot.event
async def on_ready():
    print(f'{bot.user.name} ha iniciado sesión en Discord!')

@bot.command()
async def predict(ctx, *, args):
    # Suponemos que los argumentos se pasan como una cadena delimitada por comas
    data_list = args.split(',')
    input_data = {
        'Country': data_list[0],
        'City': data_list[1],
        'CO AQI Value': int(data_list[2]),
        'Ozone AQI Value': int(data_list[3]),
        'NO2 AQI Value': int(data_list[4]),
        'PM2.5 AQI Value': int(data_list[5]),
        'AQI Category': data_list[6],
        'CO AQI Category': data_list[7],
        'Ozone AQI Category': data_list[8],
        'NO2 AQI Category': data_list[9],
        'PM2.5 AQI Category': data_list[10],
        'Date Time': data_list[11]
    }
    predicted_value = make_prediction(input_data)

    if predicted_value <= 50:
        calidad_aire = "buena"
    elif predicted_value <= 100:
        calidad_aire = "moderada"
    else:
        calidad_aire = "mala"

    response = f"Predicción de Calidad del Aire para {input_data['City']}, {input_data['Country']} el {input_data['Date Time']}: El valor AQI predicho es aproximadamente {predicted_value}, lo cual indica una calidad de aire {calidad_aire}."
    await ctx.send(response)

bot.run('https://discord.com/api/webhooks/1243106155174035486/lWB3cHX69Q1DyuMPQZ7uXLlYqvPPmTwmFpN-IByz1IaSgjG_9dtXP-atei_RO00nhG1W')
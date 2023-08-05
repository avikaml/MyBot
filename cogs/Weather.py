import discord
from discord.ext import commands
import requests
import datetime

# API Key:
# 89f8d62346f0eee5b7e94ad7363dc88b
# Might wanna add to .env or something to hide it!! or thorugh settings.py

class Weather(commands.Cog):

    def __init__(self, client, api_key):
        self.client = client
        self.api_key = api_key

    @commands.Cog.listener() # Decorator
    async def on_ready(self):
        print('Weather.py is ready')

    @commands.command(alias=["Weather","WEATHER","wEATHER"])
    async def weather(self, ctx, *, city_name):
        try:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api_key}'
            response = requests.get(url)
            data = response.json()

            if data['cod'] == 200:
                # Make an HTTP GET request using the requests library(The response is a json)
                weather_info = data['weather'][0]['description']
                temperature_kelvin = data['main']['temp']
                temperature_celsius = temperature_kelvin - 273.15
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                # Convert sunrise and sunset timestamps to human-readable times
                sunrise_timestamp = data['sys']['sunrise']
                sunset_timestamp = data['sys']['sunset']
                sunrise_time = datetime.datetime.fromtimestamp(sunrise_timestamp).strftime('%H:%M:%S')
                sunset_time = datetime.datetime.fromtimestamp(sunset_timestamp).strftime('%H:%M:%S')


                # Create an embed
                embed = discord.Embed(title=f"Weather in {city_name}", color=discord.Color.blue())
                embed.add_field(name=":partly_sunny: Description", value=weather_info, inline=False)
                embed.add_field(name=":thermometer: Temperature", value=f"{temperature_celsius:.1f}°C", inline=False)
                embed.add_field(name=":droplet: Humidity", value=f"{humidity}%", inline=False)
                embed.add_field(name=":wind_blowing_face: Wind Speed", value=f"{wind_speed} m/s", inline=False)
                embed.add_field(name=":sunrise_over_mountains: Sunrise", value=sunrise_time, inline=False)
                embed.add_field(name=":city_sunset: Sunset", value=sunset_time, inline=False)
                embed.set_footer(text="Weather data from OpenWeatherMap")


                await ctx.send(embed=embed)
            else:
                await ctx.send(f"Error: Unable to fetch weather data for {city_name}.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
    

async def setup(client):
    api_key = '89f8d62346f0eee5b7e94ad7363dc88b'
    await client.add_cog(Weather(client, api_key))
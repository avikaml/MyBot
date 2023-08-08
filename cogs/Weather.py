import discord
from discord.ext import commands
import requests
import datetime
import pytz
import settings
import SingletonLogger
from settings import weather_api_key

''' This had sensitive info - weather api key '''

logger = SingletonLogger.get_logger()

class Weather(commands.Cog):
    def __init__(self, client, api_key):
        self.client = client
        self.api_key = api_key

    @commands.Cog.listener() # Decorator
    async def on_ready(self):
        print('Weather.py is ready')

    @commands.command(alias=["Weather","WEATHER","wEATHER"])
    async def weather(self, ctx, *, city_name=None):
        if city_name is None:
            await ctx.send("Please specify a city name")
            logger.warning(f"User: {ctx.author} (ID: {ctx.author.id}) did not specify a city name in {ctx.guild.name} (ID: {ctx.guild.id})")
            return

        logger.info(f"User: {ctx.author} (ID: {ctx.author.id}) used the weather command in {ctx.guild.name} (ID: {ctx.guild.id})")
        # Make an HTTP GET request using the requests library(The response is a json)
        try:
            city_name = city_name.title()
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={self.api_key}'
            response = requests.get(url)
            data = response.json()

            if data['cod'] == 200:
                # Get the weather info from the json response
                weather_info = data['weather'][0]['description']
                temperature_kelvin = data['main']['temp']
                temperature_celsius = temperature_kelvin - 273.15
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']

                # Convert sunrise and sunset timestamps to the local time of the city
                sunrise_timestamp = data['sys']['sunrise']
                sunset_timestamp = data['sys']['sunset']
                sunrise_time = datetime.datetime.fromtimestamp(sunrise_timestamp, pytz.timezone(pytz.country_timezones(data['sys']['country'])[0])).strftime('%H:%M:%S')
                sunset_time = datetime.datetime.fromtimestamp(sunset_timestamp, pytz.timezone(pytz.country_timezones(data['sys']['country'])[0])).strftime('%H:%M:%S')

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
            logger.info(f"An error occurred: {e}")

async def setup(client):
    await client.add_cog(Weather(client, weather_api_key))
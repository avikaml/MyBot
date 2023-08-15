import discord
from discord.ui import Button, View
from discord.ext import commands

# WIP
class Pagination(View):
    def __init__(self, pages, username, user_profile_url):
        super().__init__()
        self.pages = pages
        self.current_page = 0
        self.message = None
        self.username = username
        self.user_profile_url = user_profile_url

    async def show_page(self, interaction: discord.Interaction, button: discord.ui.Button = None):
        page = self.pages[self.current_page*10:(self.current_page + 1)*10] # test
        page = "\n".join(page)
        embed = discord.Embed(title=f"{self.username}'s recent tracks",
                url=f"{self.user_profile_url}",
                color=discord.Color.default()
                , description=page)
        embed.set_author(name=f"LastFM", icon_url='https://images-ext-2.discordapp.net/external/yXB4N2dn_VX55UFo4EUH-rdq3JZs7Mo04nYbYiHbhF4/https/i.imgur.com/UKJPKD5.png')
        #page_number = int((self.current_page + 1)/(len(self.pages)/10))
        embed.set_footer(text=f"Page {self.current_page+1}")

        if interaction:
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="<<")
    async def first_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = 0
        await self.show_page(interaction=interaction)
    
    @discord.ui.button(label="<")
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page == 0:
            self.current_page = int(len(self.pages)/10) - 1
        else:
            self.current_page -= 1
        
        await self.show_page(interaction=interaction)
    
    @discord.ui.button(label=">")
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.current_page == int(len(self.pages)/10) - 1:
            self.current_page = 0
        else:
            self.current_page += 1
        
        await self.show_page(interaction=interaction)
    
    @discord.ui.button(label=">>")
    async def last_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = int(len(self.pages)/10) - 1
        await self.show_page(interaction=interaction)
    
    async def on_timeout(self):
        try:
            await self.message.delete() # error...
        except discord.NotFound: 
            pass


import discord
from discord.ui import Button, View
from discord.ext import commands

# WIP
class Pagination(View):
    def __init__(self, pages):
        super().__init__()
        self.pages = pages
        self.current_page = 0
        self.message = None

    async def show_page(self, interaction: discord.Interaction, button: discord.ui.Button = None):
        page = self.pages[self.current_page*10:(self.current_page + 1)*10] # test
        print(self.pages[0])
        print(page)
        embed = discord.Embed(title=f"Page {self.current_page + 1}/{len(self.pages)}", description=page)
        
        if len(self.pages) > 1:
            embed.set_footer(text=f"Use the buttons to navigate between pages.")

        if interaction:
            await interaction.response.edit_message(embed=embed, view=self)
        """ else:
            self.message = await interaction.response.send_message(embed=embed, view=self) """

    @discord.ui.button(label="<<")
    async def first_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.current_page = 0
        await self.show_page(interaction=interaction)
    
    @discord.ui.button(label="<")
    async def previous_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.current_page == 0:
            self.current_page = len(self.pages) - 1
        else:
            self.current_page -= 1
        
        await self.show_page(interaction=interaction)
    
    @discord.ui.button(label=">")
    async def next_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        if self.current_page == len(self.pages) - 1:
            self.current_page = 0
        else:
            self.current_page += 1
        
        await self.show_page(interaction=interaction)
    
    @discord.ui.button(label=">>")
    async def last_page(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.current_page = len(self.pages) - 1
        await self.show_page(interaction=interaction)
    
    async def on_timeout(self):
        try:
            await self.message.delete() # error...
        except discord.NotFound: 
            pass


Sept. 2024: This is a project I made in summer of 2023 after my first year of SE studies. It no longer works due to several reasons but i plan on fixing it in the future. The biggest part of this bot is the LastFM integration - check the relevant Cog to see more :)

The following is from august 2023:

This is a bot that I'm making for fun that works on discord servers!

At the moment, the default bot command prefix is '!'
Please make sure the bot is online before adding it your server.

Current Features: 
1. Hello/Goodbye message when a user Joins/Leaves 
2. !hello message which triggers a greeting from the bot 
3. Basic embed 
4. Moderation features - clear messages, kick, ban, unban
5. Customizable prefixe with !setprefix command - Hasn't  been tested yet
-- Starting here, each(significant) feature will be worked on in a separate branch --
6. Logging
7. !weather {cityname} command that fetches the current weather for a specified city using the OpenWeatherMap API
8. !avatar @username command that displays the avatar of the specified user
9. SQL database to store information - mostly lf related stuff as of now
10. !tweet command that embeds tweets, is currently broken due to twitter shenanigans, instead !vx exists
11. lastfm commands, currently there exist: lfset, lfchange(temporary, should be part of lfset), !lf np, !lfrecent, !lftoptracks - time period, !lfartist(broken atm!), !lftopalbums, !lftopartists
12. Many fun commands to display gifs and images


Planned Features:
2. LastFM integration - !lfartist - need to fix, !lfchart - if provided by the API, and need to fix up code to be more modular, !lftrack to get track info
3. Spotify integration? 
4. Starboard integration
5. Tests
6. level system
7. Error handling/Custom error messages?
8. Slash commands
9. !userinfo command
10. aiohttp usage throught the whole project
11. !rep system

Next features to work on: Level system, Starboard, rep system, fix up lastfm stuff

Additional notes for myself:
- LastFM commands could do with a redo - need to modulize them and reasses where i have code duplication and api calls without aiohttp

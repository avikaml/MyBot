This is a bot that I'm making for fun that works on discord servers!

At the moment, the deafult bot command prefix is '!'
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


Planned Features:
1. Embeds for gifs, etc
2. Block certain words - a la delete the forbidden message and post a warning to that user 
3. LastFM integration - !lfartist - need to fix, !lfchart - if provided by the API, and need to fix up code to be more modular, !lftrack to get track info
4. Spotify integration? 
5. Starboard integration
6. Tests
7. Lots of fun commands that display certain pictures/gifs and more
8. level system
9. Error handling/Custom error messages?
10. Birthday Messages
11. Slash commands
12. !userinfo command
13. add logger to all the cogs so they log
14. !tiktok command for tiktok embeds with vx
15. aiohttp

Next features to work on: 7, 8, 1, 2 (Not necessarily in that order)

Additional notes for myself:
- LastFM commands could do with a redo - need to modulize them and reasses where i have code duplication and api calls without aiohttp


\\ NOTE TO SELF: Before making the repo public, must delete the history of main.py and apikeys.py, possibly Twitter.py(that I deleted and will reinstate, not sure if I actually did commit it) and Weather.py . Good practice for github ^-^

\\ \\ UPDATE: I could possibly just reset the bot token, twitter tokens  and weather token and that will be enough instead of going through github deletion.
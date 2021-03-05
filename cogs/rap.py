import requests
import json
import datetime

from discord.ext import commands, tasks


class Rap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_rap_date.start()
        self.done = []

    async def gds(self):
        channels = []
        for guild in self.bot.guilds:
            [channels.append(x) for x in guild.channels if x.name == "zemo-bot"]

        return channels

    @tasks.loop(seconds=30.0)
    async def check_rap_date(self):
        now = datetime.datetime.now()
        if datetime.datetime.now().strftime("%A") == "Friday" and int(now.hour) == 00 and int(now.minute) > 5:
            await self.rap()

    async def rap(self):
        today = str(datetime.datetime.now().strftime("%d.%m.%Y"))
        if today not in self.done:
            url = "https://deinupdate-api.azurewebsites.net/api/v2/news?interests=4"
            x = requests.get(url, headers={"user-agent": "okhttp/4.8.1"})
            id = [x for x in json.loads(x.content.decode())["items"] if x["title"] == "Alle Rap-Songs, die heute erschienen sind!"][0]["id"]
            get_item = f"https://deinupdate-api.azurewebsites.net/api/v2/news/{id}"
            x = requests.get(get_item, headers={"user-agent": "okhttp/4.8.1"})
            items = json.loads(x.content.decode())["content"]
            item_single = [items[items.index(x) + 1] for count, x in enumerate(items) if items[count]['value'] == 'SINGLES'][0]

            channels = await self.gds()
            for x in channels:
                await x.send("Alle Rap Songs die heute erschienen sind: \n" + item_single["value"].replace("<em>", "").replace("<br>", "").replace("</em>", "").replace("<i>", "").replace("</i>", ""))

            self.done.append(today)


def setup(bot):
    bot.add_cog(Rap(bot))

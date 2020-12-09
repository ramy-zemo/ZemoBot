import requests

req = requests.get("https://deinupdate-api.azurewebsites.net/api/v2/news")

lite = req.json()["items"]

neuen_songs = [x for x in lite if x["title"] == 'Alle Rap-Songs, die heute erschienen sind!']

new_url = "https://deinupdate-api.azurewebsites.net/api/v2/news/180556"

item = requests.get(new_url)
#print(item.json()["content"][4]["value"].replace("<em>", "").replace("</em>", "").replace("<br>", ""), sep="\n")
print(item.json()["content"][6]['value'].replace("<em>", "").replace("</em>", "").replace("<br>", ""), sep="\n")
#print(neuen_songs[0])

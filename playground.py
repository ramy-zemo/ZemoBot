import requests

it = requests.post("https://id.twitch.tv/oauth2/token?client_id=qw6mmjkdrazpzl4odsmgj40bd6i7wd&client_secret=bb87yhllvarj73h4c61ttqskzmoefn")
print(it.content)
#print(it.headers)



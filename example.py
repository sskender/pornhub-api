import pornhub

search_keywords = []

#client = pornhub.PornHub(search_keywords, "5.135.164.72", 3128)
#With proxy, given a Proxy IP and Port. For the countries with restricted access like Turkey, etc.

client = pornhub.PornHub(search_keywords)

for star in client.getStars(10):
    print(star)
    print(star["name"])
    
for video in client.getVideos(10,page=2):
    print(video)
    print(video["title"])

for gif in client.getGifs(10,page=2):
    print(gif)
    print(gif["mp4"])

for photo_url in client.getPhotos(5):
    print(photo_url)

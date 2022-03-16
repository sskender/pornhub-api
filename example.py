import pornhub

search_keywords = []

#client = pornhub.PornHub("5.135.164.72", 3128, search_keywords)
#With proxy, given a Proxy IP and Port. For the countries with restricted access like Turkey, etc.

client = pornhub.PornHub(search_keywords)

for star in client.getStars(10):
    print(star)
    print(star["name"])
    
for video in client.getVideos(10,page=2):
    print(video)

for photo_url in client.getPhotos(5):
    print(photo_url)

video = client.getVideo("SOME VIDEO URL")
print(video)
print(video['accurate_views'])

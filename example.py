import pornhub

search_keywords = []
client = pornhub.PornHub(search_keywords)

for star in client.getStars(10):
    print star
    print star["name"]
    
for video in client.getVideos(10,page=2):
    print video
    
for photo_url in client.getPhotos(5):
    print photo_url
    
print "All done!"

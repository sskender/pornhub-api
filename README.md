# PornHub Unofficial API
Unofficial API for pornhub.com in Python

## Usage

#### Create client
```python
import pornhub
client = pornhub.PornHub()
```

#### Grab stars
```python
for star in client.getStars(10):
    print star
    print star["name"]
```

#### Create client with search keywords
```python
keywords = ["word1", "word2"]
client = pornhub.PornHub(keywords)

for video in client.getVideos(10,page=2):
    print video
    print video["url"]
```

## License
MIT license

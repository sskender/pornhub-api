# PornHub Unofficial API

Unofficial API for pornhub.com in Python

### *Pull requests are welcome!!!*

I find it quite difficult to make time for an active development on this project, so I will be more than happy to merge your pull requests. Thank you all for supporting this project!

## Install

```bash
pip3 install pornhubapi
```

## How to use

#### Create client

```python
import pornhub
client = pornhub.PornHub()
```

#### Create client with proxy

```python
import pornhub
# With proxy, given a Proxy IP and Port. For the countries with restricted access like Turkey, etc.
client = pornhub.PornHub("5.135.164.72", 3128)
```

#### Grab stars

```python
for star in client.getStars(10):
    print(star)
    print(star["name"])
```

#### Create client with search keywords

```python
keywords = ["word1", "word2"]
client = pornhub.PornHub(keywords)

# if using a proxy
client = pornhub.PornHub(keywords, "5.135.164.72", 3128)
# or
client = pornhub.PornHub(ProxyIP="5.135.164.72", ProxyPort=3128, keywords=["word1", "word2"])

for video in client.getVideos(10, page=2):
    print(video)
    print(video["url"])
```

#### Sort Video by parameter

When keywords are set: `view`, `rate`, `long`, `recent` 
```python
keywords = ["word1", "word2"]
client = pornhub.PornHub(keywords)

for video in client.getVideos(10, page=2, sort_by="long"):
    print(video)
    print(video["url"])
```

When keywords are not set: `view`, `rate`, `long`, `new`, `hot`
```python
client = pornhub.PornHub()

for video in client.getVideos(10, page=2, sort_by="hot"):
    print(video)
    print(video["url"])
```

#### Get more information about the single video

Method **getVideo(url, viewkey)** gives more detail information about a single video

```python
client = pornhub.PornHub()

# You can input the full video url, like that
video = client.GetVideo("https://www.pornhub.com/view_video.php?viewkey=SOMEKEY")
# Or that
video = client.GetVideo(url="https://www.pornhub.com/view_video.php?viewkey=SOMEKEY")
# Or input only viewkey, like that
video = client.GetVideo(viewkey="SOMEKEY")

print(video)
print(video["url"])
```

The method return a dictionary with keywords:
1. *"title"* (type: string) - Video title
2. *"views"* (type: string) - Rounded number of views, for example "2M"
3. *"accurate_views"* (type: integer) - Full number of views, for example "123456789". When video don't have many views "views"="accurate_views"
4. *"rating"* (type: integer) - Video rating in percent
5. *"duration"* (type: string) - Video duration in format "hh:mm:ss"
6. *"loaded"* (type: string) - When the video was uploaded, for example "2 months ago"
7. *"upload_date"* (type: string) - Video upload date in format "yyyy-mm-dd"
8. *"likes"* (type: string) - Similar like *"views"*
9. *"accurate_likes"* (type: integer) - Similar like *"accurate_views"*
10. *"dislikes"* (type: string) - Similar like *"views"*
11. *"accurate_dislikes"* (type: integer) - Similar like *"accurate_views"*
12. *"favorite"* (type: string) - How many times added to favorites, rounded. For example "2K"
13. *"author"* (type: string) - Video author (channel)
14. *"pornstars"* (type: list) - Video stars
15. *"categories"* (type: list) - Video categories
16. *"tags"* (type: list) - Video tags
17. *"production"* (type: string) - Video production (Professional or Homemade)
18. *"img_url"* (type: string) - URL to Preview Image of Video
19. *"embed_url"* (type: string) - URL to Video Player

If the video is not available in your country, in **"title"** will **"Video not available in your country"**, in in others keys will **"None"**

**getVideo()** method can be well combined with **getVideos()**
```python
keywords = ["word1", "word2"]
client = pornhub.PornHub(keywords)

for video in client.getVideos(10, page=2, sort_by="hot"):
  video_data = client.getVideo(video["url"])
  print(video_data["title"], video_data["views"])
```

## Contributors

<table>
  <tr>
    <td align="center"><a href="https://github.com/SashaSZ"><img src="https://avatars.githubusercontent.com/u/88130296?v=4" width="100px;" alt=""/><br /><sub><b>SashaSZ</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/CprogrammerIbrahim"><img src="https://avatars1.githubusercontent.com/u/40497100?s=400&v=4" width="100px;" alt=""/><br /><sub><b>Ibrahim Ipek</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/kittinan"><img src="https://avatars0.githubusercontent.com/u/144775?s=400&v=4" width="100px;" alt=""/><br /><sub><b>Kittinan</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/fantomnotabene"><img src="https://avatars2.githubusercontent.com/u/9576189?s=460&u=7a9639ad287e7070220b22975dbab87b0228611f&v=4" width="100px;" alt=""/><br /><sub><b>Елизаров Роман Русланович</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/IThinkImOKAY"><img src="https://avatars3.githubusercontent.com/u/61555147?s=460&u=34c57df77de20121b0e298effe4092e32dd16ee1&v=4" width="100px;" alt=""/><br /><sub><b>IThinkImOKAY</b></sub></a><br /></td>
  </tr>
<table>

## License

MIT license

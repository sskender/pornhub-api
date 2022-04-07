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

#### Grab Stars

```python
for star in client.getStars(10, 2):
    print(star)
    print(star["name"])
```
The method `getStars` return list of dictionary with keywords:
1. `name` (type: string) - Star name
2. `rank` (type: integer) - Star rank
3. `type` (type: string) - Star type (Pornstar or Model)
4. `videos` (type: integer) - Video quantity
5. `views` (type: string) - Rounded views number, for example "2M"
6. `verified` (type: bool) - If the Star page is verified, will have `True`
7. `trophy`(type: bool) - If the Star have trophy, will have `True`
8. `url` (type: string) - Star page URL
9. `photo` (type: string) - Star photo URL

#### Get information about the single Star

Method `getStar(url)` gives detail information about a single star
```python
client = pornhub.PornHub()
star = client.getStar("SOME STAR URL")

print(star)
print(video["name"])
```

The method return a dictionary with keywords:
1. `name` (type: string) - Star name
2. `rank` (type: integer) - Star rank
3. `ranks` (type: dictionary) - Contains all ranks like `Weekly Rank`, `Monthly Rank` and etc.
4. `type` (type: string) - Star type (Pornstar or Model)
5. `videos` (type: integer) - Video quantity
6. `views` (type: string) - Rounded views number, for example "2M"
7. `accurate_views` (type: integer) - Full views number, for example "123456789"
8. `verified` (type: bool) - If the Star page is verified, will have `True`
9. `trophy`(type: bool) - If the Star have trophy, will have `True`
10. `url` (type: string) - Star page URL
11. `photo` (type: string) - Star photo URL
12. `cover` (type: string) - Star cover image URL
13. `subs` (type: string) - Rounded followers number. For example "2K"
14. `about` (type: string) - Information about the Star
16. `infos` (type: dictionary) - Contains Star info like `Relationship status`, `Gender` and etc.
17. `socials` (type: dictionary) - Contains Star socials like `Instagram`, `Twitter` and etc.
18. `geo_block` (type: bool) - If the star page is not available in your country, will have `True`, and in others keys (excluding `url`, `name` and `type`) will `None`

Some star have old page format, so they don't have some attributes, for example `socials` and `cover`. Or they just didn't fill out them. Therefore, there will be `None`

#### Take full information about all stars

Argument `full_data` allows to get more information about the star, but its much more slower due to every page needs to be opened
```python
for star in client.getStars(10, 2, full_data=True):
    print(star)
    print(star["socials"])
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

#### Get information about the single Video

Method `getVideo(url, viewkey)` gives more detail information about a single video

```python
client = pornhub.PornHub()

# You can input the full video url, like that
video = client.getVideo("SOME PH VIDEO URL")
# Or that
video = client.getVideo(url="SOME PH VIDEO URL")
# Or input only viewkey, like that
video = client.getVideo(viewkey="SOME VIDEO KEY")

print(video)
print(video["title"])
```

The method return a dictionary with keywords:
1. `title` (type: string) - Video title
2. `views` (type: string) - Rounded views number, for example "2M"
3. `accurate_views` (type: integer) - Full views, for example "123456789"
4. `rating` (type: integer) - Video percent rating
5. `duration` (type: string) - Video duration in format "hh:mm:ss"
6. `loaded` (type: string) - How long ago the video was uploaded, for example "2 months ago"
7. `upload_date` (type: string) - Video upload date in format "yyyy-mm-dd"
8. `likes` (type: string) - Similar like `views`
9. `accurate_likes` (type: integer) - Similar like `accurate_views`
10. `dislikes` (type: string) - Similar like `views`
11. `accurate_dislikes` (type: integer) - Similar like `accurate_views`
12. `favorite` (type: string) - Rounded number of added to favorites. For example "2K"
13. `author` (type: string) - Video author (channel)
14. `pornstars` (type: list) - Video stars
15. `categories` (type: list) - Video categories
16. `tags` (type: list) - Video tags
17. `production` (type: string) - Video production (Professional or Homemade)
19. `url` (type: string) - Video URL
18. `img` (type: string) - Preview Image URL
19. `embed` (type: string) - Video embed URL
20. `geo_block` (type: bool) - If the video is not available in your country, will have `True`, and in others keys (excluding `url`) will `None`

#### Take full information about all Videos
Argument `full_data` allows you to get complete information about the video, but its much more slower due to every page needs to be opened

```python
keywords = ["word1", "word2"]
client = pornhub.PornHub(keywords)

for video in client.getVideos(10, page=2, full_data=True):
  print(video)
  print(video["upload_date"])
```

#### Grab Gifs
```python
for gif in client.getGifs(10, 2):
    print(gif)
    print(gif["mp4"])
```
The method `getGifs` return list of dictionary with keywords:
1. `title` (type: string) - Gif title
2. `url` (type: string) - Gif PH page URL
3. `embed` (type: string) - Gif embed URL
4. `img` (type: string) - Gif Image URL
5. `gif` (type: string) - Gif URL
6. `mp4` (type: string) - MP4 URL
7. `webm` (type: string) - Webm URL

Argument `full_data` allows to get more information about the gif
```python
for gif in client.getGifs(10, 2, full_data=True):
    print(gif)
    print(star["original_url"])
```
The method `getGifs` return list of dictionary with keywords:
1. `title` (type: string) - Gif title
2. `url` (type: string) - Gif PH page URL
3. `img` (type: string) - Gif Image URL
4. `gif` (type: string) - Gif URL
5. `mp4` (type: string) - MP4 URL
6. `webm` (type: string) - Webm URL
7. `embed` (type: string) - Gif embed URL
8. `views` (type: integer) - Gif views number
9. `rate` (type: integer) - Gif percent rating
11. `stars` (type: list) - Gif stars list
12. `tags` (type: list) - Gif tags list
13. `loaded` (type: string) - How long ago the gif was uploaded, for example "2 months ago"
14. `original_title` (type: string) - Original video title
15. `original_url` (type: string) - Original video URL

#### Search sorting
The following arguments are available for `Videos` sorting:
1. `sort_by`
  - If keywords are set: `view`, `rate`, `long`, `recent`
  - If keywords are not set: `view`, `rate`, `long`, `new`, `hot`
2. `period`: `day`, `week`, `month`, `year`, `all`  
    The `period` is worked when `sort_by` is `view` or `rate`
3. `region` - Alpha-2 county code like `us`, `cz` and etc.  
    The `region` is worked when `sort_by` is `view` or `hot` and keywords are not sets

Can be specified when the `client` initializing or when using the `getVideos` method.
Examples:
1. When keywords are sets
```python
keywords = ["word1", "word2"]
# All time most viewed videos
client = pornhub.PornHub(keywords, sort_by="view", period="all")
for video in client.getVideos(10, page=2):
    print(video["views"])

# Or
client = pornhub.PornHub(keywords)
for video in client.getVideos(10, page=2, sort_by="view", period="all"):
    print(video["views"])

# Or
client = pornhub.PornHub(keywords, sort_by="view")
for video in client.getVideos(10, page=2, , period="all"):
    print(video["views"]) 
```

2. When keywords are not sets
```python
# Daily most viewed video in Argentina
client = pornhub.PornHub(sort_by="view", period="day", region="ar")
for video in client.getVideos(10, page=2):
    print(video["views"])
```

The following arguments are available for `Stars` sorting:
1. `sort_by` : `popular`, `view`, `trend`, `subs`, `alpha`, `videos`, `random`  
    When sorting alphabetically, you can select a letter using a keyword `letter`, that can be `a`-`z` or `num`
2. `period`: `week`, `month`, `year`  
    The `period` is worked when `sort_by` is `popular` or `view`
3. `p_type`: `pornstars` or `models`  


```python
# This year most viewed Stars
client = pornhub.PornHub(sort_by="view", period="year")
for star in client.getStars(10, page=2):
    print(star)

# Alphabetical sorting starting from numbers
for star in client.getStars(10, page=2, sort_by="alpha", letter="num"):
    print(star)
```

The following arguments are available for `Gifs` sorting:
1. `sort_by` : `recent`, `view`, `rate`
2. `period`: `day`, `week`, `month`, `all`  
    The `period` is worked when `sort_by` is `view` or `rate`

```python
keywords = ["word1", "word2"]
# All time most viewed Gifs
client = pornhub.PornHub(keywords, sort_by="view", period="all")
for gif in client.getGifs(10, 2):
    print(gif["mp4"])
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

# PornHub Unofficial API

Unofficial API for pornhub.com in Python

*Pull requests are welcome!!!*

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
client = pornhub.PornHub("5.135.164.72", 3128)
#With proxy, given a Proxy IP and Port. For the countries with restricted access like Turkey, etc.
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
client = pornhub.PornHub(keywords=keywords)

# if using a proxy
client = pornhub.PornHub("5.135.164.72", 3128, keywords)
# or
client = pornhub.PornHub(ProxyIP="5.135.164.72", ProxyPort=3128, keywords=["word1", "word2"])

for video in client.getVideos(10,page=2):
    print(video)
    print(video["url"])
```

#### Sort Video by parameter

When keywords are set: "view", "rate", "long", "recent" 
```python
keywords = ["word1", "word2"]
client = pornhub.PornHub(keywords=keywords)

for video in client.getVideos(10,page=2, sort_by="long"):
    print(video)
    print(video["url"])
```

When keywords are not set: "view", "rate", "long", "new", "hot"
```python
client = pornhub.PornHub()

for video in client.getVideos(10,page=2, sort_by="hot"):
    print(video)
    print(video["url"])
```

## Contributors

<table>
  <tr>
    <td align="center"><a href="https://github.com/CprogrammerIbrahim"><img src="https://avatars1.githubusercontent.com/u/40497100?s=400&v=4" width="100px;" alt=""/><br /><sub><b>Ibrahim Ipek</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/kittinan"><img src="https://avatars0.githubusercontent.com/u/144775?s=400&v=4" width="100px;" alt=""/><br /><sub><b>Kittinan</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/fantomnotabene"><img src="https://avatars2.githubusercontent.com/u/9576189?s=460&u=7a9639ad287e7070220b22975dbab87b0228611f&v=4" width="100px;" alt=""/><br /><sub><b>Елизаров Роман Русланович</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/IThinkImOKAY"><img src="https://avatars3.githubusercontent.com/u/61555147?s=460&u=34c57df77de20121b0e298effe4092e32dd16ee1&v=4" width="100px;" alt=""/><br /><sub><b>IThinkImOKAY</b></sub></a><br /></td>
  </tr>
<table>

## License

MIT license

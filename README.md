# PornHub Unofficial API

Unofficial API for pornhub.com in Python

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
client = pornhub.PornHub(keywords)

for video in client.getVideos(10,page=2):
    print(video)
    print(video["url"])
```

## Contributors

<table>
  <tr>
    <td align="center"><a href="https://github.com/CprogrammerIbrahim"><img src="https://avatars1.githubusercontent.com/u/40497100?s=400&v=4" width="100px;" alt=""/><br /><sub><b>Ibrahim Ipek</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/kittinan"><img src="https://avatars0.githubusercontent.com/u/144775?s=400&v=4" width="100px;" alt=""/><br /><sub><b>Kittinan</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/fantomnotabene"><img src="https://avatars2.githubusercontent.com/u/9576189?s=460&u=7a9639ad287e7070220b22975dbab87b0228611f&v=4" width="100px;" alt=""/><br /><sub><b>Елизаров Роман Русланович</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/Mr-Steal-Your-Script"><img src="https://avatars3.githubusercontent.com/u/61555147?s=460&u=34c57df77de20121b0e298effe4092e32dd16ee1&v=4" width="100px;" alt=""/><br /><sub><b>Mr-Steal-Your-Script</b></sub></a><br /></td>
  </tr>
<table>

## License

MIT license

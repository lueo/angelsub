AngelSub
===

Subtitle downloader do it right.

Intro
---

Just get me subtitles. In a clean way.

**TL;DR**

```sh
$ cd "What Ever Scary Movie \(2012\)"
$ angelsub .
$ ls
What Ever Scary Movie.avi
What Ever Scary Movie.eng.srt
What Ever Scary Movie.chs.srt
```

Usage
---

### CLI

```bash
# Download and organize all subtitles of movies in the current directory.
$ angelsub .
# Download and organize all subtitles of a movie.
$ angelsub "Lord of the ring I.avi"
# Organize local subtitles of a movies.
$ angelsub --org 'Tick.Tock.(2013)-BDRip.avi'
# Download subtitles. (Existing ones will be renamed)
$ angelsub --download 'Push.(2012)-DVDRip.mp4'
```

### API

```python
>>> import angelsub
# This will read possible local subtitles in memory automatically.
>>> vf = angelsub.VideoFile('/media/Video/Terrible.Movie.(2024).mp4')
# Show local subtitles.
>>> vf.subs.local_subs
# Get subtitles from *shooter.cn*
>>> vf.subs.get_shooter_subs()
# You got at most 3 subtitles in memory now.
>>> vf.subs.shooter_subs
# Compare all subtitles and delete duplicates.
# __(Caution: Existing subtitles will be renamed.)__
>>> vf.subs.organize()
# Write them all to disk
>>> vf.subs.sync()
```

### GUI

(Not yet. Prepare to write it with PyQt4.)

Installation
---

### Linux (Ubuntu)
```bash
$ git clone https://github.com/lueo/angelsub
$ cd angelsub
$ pip install -r requirements.txt
$ angelsub --version
```
### Requirement

1. requests
2. chardet
3. mafan

Note
---

All subtitles will be converted to UTF-8.

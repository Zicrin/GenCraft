# Ignify

** Ignify** is a flawless Minecraft-style username generator written in Python.  
Generates clean, aesthetic usernames with only letters — no numbers, no symbols — and checks their availability in real time.

---

## ✨ Features

- Generates usernames from **3 to 8 characters**
- **Letters only** — no numbers or symbols
- Checks if usernames are **available**
- Adjustable delay to avoid rate-limiting
- Optional flag to show **taken** usernames
- Generate username and validates them so fast you cant even see it happening.
- 
---

## 📦 Requirements

- Python 3.8+
- `requests` library


How to install ?
Install with:

```bash
git clone https://github.com/zicrin/Ignify.git
```

Clone the repository.

```bash
cd Ignify
```
Move into Ignify folder.
 
```bash
usage: ignify.py [-h] [-n COUNT] [--min MIN] [--max MAX] [--delay DELAY] [--show-taken]

🧠 Flawless Minecraft Username Generator (NO NUMBERS)

options:
  -h, --help         show this help message and exit
  -n, --count COUNT  Number of available usernames to find
  --min MIN          Minimum username length
  --max MAX          Maximum username length
  --delay DELAY      Delay between API requests (seconds)
  --show-taken       Show taken usernames too
```
Usage and how to uuse the tool.

```bash
python ignify.py -n 5 --min 4 --max 6 --delay 0.3 --show-taken
```
Example of how to use the tool.

[![Watch the video](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)]([https://www.youtube.com/watch?v=VIDEO_ID](https://www.youtube.com/watch?v=P5RsfA8kYjA))

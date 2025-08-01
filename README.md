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

Install with:

```bash
git clone https://github.com/zicrin/gencraft.git
cd GenCraft
```
Easy and simple
Clone the repository 
 
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

```bash
python GenCraft.py -n 5 --min 4 --max 6 --delay 0.3 --show-taken
```

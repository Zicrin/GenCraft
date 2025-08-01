# GenCraft

**🧠 GenCraft** is a flawless Minecraft-style username generator written in Python.  
Generates clean, aesthetic usernames with only letters — no numbers, no symbols — and checks their availability in real time.

---

## ✨ Features

- Generates usernames from **3 to 8 characters**
- **Letters only** — no numbers or symbols
- Checks if usernames are **available**
- Adjustable delay to avoid rate-limiting
- Optional flag to show **taken** usernames

---

## 📦 Requirements

- Python 3.8+
- `requests` library

Install with:

```bash
git clone https://github.com/your-username/gencraft.git
cd GenCraft
```

 
```bash
usage: GenCraft.py [-h] [-n COUNT] [--min MIN] [--max MAX] [--delay DELAY] [--show-taken]

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

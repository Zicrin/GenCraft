import random
import string
import requests
import time
import argparse
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta

init(autoreset=True)
MOJANG_API = "https://api.mojang.com/users/profiles/minecraft/{}"
MAX_THREADS = 10

VOWELS = "aeiou"
CONSONANTS = ''.join(set(string.ascii_lowercase) - set(VOWELS))

def print_ascii_banner():
    banner = r"""
  ________              _________                _____  __   
 /  _____/  ____   ____ \_   ___ \____________ _/ ____\/  |_ 
/   \  ____/ __ \ /    \/    \  \/\_  __ \__  \\   __\\   __\
\    \_\  \  ___/|   |  \     \____|  | \// __ \|  |   |  |  
 \______  /\___  >___|  /\______  /|__|  (____  /__|   |__|  
        \/     \/     \/        \/            \/             
"""
    print(Style.BRIGHT + Fore.BLUE + banner)

def readable_username(length):
    name = ""
    alt = random.choice([True, False])
    while len(name) < length:
        name += random.choice(CONSONANTS if alt else VOWELS)
        alt = not alt
    return name[:length]

def is_username_available(username):
    try:
        response = requests.get(MOJANG_API.format(username), timeout=5)
        return username, response.status_code in (204, 404)
    except requests.RequestException:
        return username, None

def generate_batch(batch_size, min_len, max_len, tried_set):
    names = set()
    while len(names) < batch_size:
        length = random.randint(min_len, max_len)
        uname = readable_username(length)
        if uname not in tried_set:
            tried_set.add(uname)
            names.add(uname)
    return list(names)

def check_batch_parallel(usernames, delay, show_taken):
    available = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(is_username_available, name) for name in usernames]
        for f in as_completed(futures):
            username, result = f.result()
            if result is None:
                print(Fore.YELLOW + f"[⚠️  SKIPPED] API error: {username}")
                continue
            if result:
                print(Fore.GREEN + f"[✅ AVAILABLE] {username}")
                available.append(username)
            elif show_taken:
                print(Fore.RED + f"[❌ TAKEN]     {username}")
            time.sleep(delay)
    return available

def generate_available_usernames(count, min_len, max_len, delay, show_taken):
    tried = set()
    found = []
    start = datetime.now()

    print(Style.BRIGHT + f"\n🔍 Finding {count} available Minecraft usernames (no numbers)...\n")

    while len(found) < count:
        batch = generate_batch(MAX_THREADS, min_len, max_len, tried)
        new_found = check_batch_parallel(batch, delay, show_taken)
        found.extend(new_found)
        eta = (datetime.now() - start) / max(1, len(found)) * (count - len(found))
        print(Fore.CYAN + f"⏳ {len(found)}/{count} found. ETA: {str(timedelta(seconds=int(eta.total_seconds())))}")

    print(Style.BRIGHT + f"\n🎉 Done! {len(found)} available usernames found.\n")
    print(Fore.CYAN + "✨ Final List:")
    for name in sorted(found)[:count]:
        print("  -", name)

def main():
    parser = argparse.ArgumentParser(description="🧠 Flawless Minecraft Username Generator (NO NUMBERS)")
    parser.add_argument("-n", "--count", type=int, default=10, help="Number of available usernames to find")
    parser.add_argument("--min", type=int, default=3, help="Minimum username length")
    parser.add_argument("--max", type=int, default=8, help="Maximum username length")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between API requests (seconds)")
    parser.add_argument("--show-taken", action="store_true", help="Show taken usernames too")
    args = parser.parse_args()

    print_ascii_banner()

    if not (3 <= args.min <= args.max <= 16):
        print(Fore.RED + "❌ Username length must be between 3 and 16.")
        return

    generate_available_usernames(args.count, args.min, args.max, args.delay, args.show_taken)

if __name__ == "__main__":
    main()

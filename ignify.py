import argparse
import requests
import string
import random
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from colorama import Fore, Style, init
import sys

init(autoreset=True)

MOJANG_API = "https://api.mojang.com/users/profiles/minecraft/{}"
MAX_THREADS = 32  # tweak this if you want less aggressive parallelism

VOWELS = "aeiou"
CONSONANTS = ''.join(set(string.ascii_lowercase) - set(VOWELS))

# === ASCII Banner ===
ASCII_BANNER = fr"""{Fore.BLACK}{Style.BRIGHT}

    .___              .__  _____       
    |   | ____   ____ |__|/ ____\__.__.
    |   |/ ___\ /    \|  \   __<   |  |
    |   / /_/  >   |  \  ||  |  \___  |
    |___\___  /|___|  /__||__|  / ____|
       /_____/      \/          \/     
{Fore.CYAN}▶Fastest Username Generator CLI
{Style.RESET_ALL}"""

# === Session Setup ===
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=3)
session.mount('https://', adapter)

# === Username Generator ===
def readable_username(length):
    name = ""
    alt = random.choice([True, False])
    while len(name) < length:
        name += random.choice(CONSONANTS if alt else VOWELS)
        alt = not alt
    return name[:length]

def generate_usernames(batch_size, min_len, max_len, used):
    names = set()
    while len(names) < batch_size:
        length = random.randint(min_len, max_len)
        uname = readable_username(length)
        if uname not in used:
            names.add(uname)
            used.add(uname)
    return list(names)

# === Availability Check ===
def check_username(username):
    try:
        r = session.get(MOJANG_API.format(username), timeout=5)
        return username, r.status_code in (204, 404)
    except requests.RequestException:
        return username, None

def check_batch_parallel(usernames):
    available = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(check_username, name) for name in usernames]
        for f in as_completed(futures):
            uname, status = f.result()
            if status:
                print(Fore.GREEN + f"[✅ AVAILABLE] {uname}")
                available.append(uname)
            elif status is False:
                print(Fore.RED + f"[❌ TAKEN]     {uname}")
            else:
                print(Fore.YELLOW + f"[⚠️  ERROR]     {uname} (skipped)")
    return available

# === Main Generator Loop ===
def find_usernames(target_count, min_len, max_len, save, json_output):
    used = set()
    found = []
    start_time = datetime.now()

    print(f"\n🔍 Searching for {target_count} available usernames...\n")

    while len(found) < target_count:
        batch = generate_usernames(MAX_THREADS * 2, min_len, max_len, used)
        result = check_batch_parallel(batch)
        found.extend(result)

        eta = (datetime.now() - start_time) / max(1, len(found)) * (target_count - len(found))
        print(Fore.CYAN + f"⏳ Progress: {len(found)}/{target_count} | ETA: {str(timedelta(seconds=int(eta.total_seconds())))}\n")

    # Output
    print(Style.BRIGHT + f"\n🎉 Done! {len(found)} usernames found.")
    print(Fore.CYAN + "\n✨ Final List:")
    for name in sorted(found[:target_count]):
        print("  -", name)

    if save:
        with open("available_usernames.txt", "w") as f:
            for name in sorted(found[:target_count]):
                f.write(name + "\n")
        print(Fore.YELLOW + "\n💾 Saved to available_usernames.txt")

    if json_output:
        print(Fore.CYAN + "\n📦 JSON Output:")
        print(json.dumps(sorted(found[:target_count]), indent=2))

    print(Fore.MAGENTA + f"\n⏱️ Total time: {str(datetime.now() - start_time)}\n")

# === Custom Help Formatter with ASCII ===
class CustomParser(argparse.ArgumentParser):
    def print_help(self, *args, **kwargs):
        print(ASCII_BANNER)
        super().print_help(*args, **kwargs)

    def error(self, message):
        print(ASCII_BANNER)
        self.print_usage(sys.stderr)
        self.exit(2, f"{Fore.RED}❌ Error: {message}\n")

# === CLI Entry Point ===
def main():
    parser = CustomParser(description="GenCraft — Blazing Fast Minecraft Username Generator")
    parser.add_argument("-n", "--count", type=int, default=10, help="How many available usernames to find")
    parser.add_argument("--min", type=int, default=3, help="Minimum username length")
    parser.add_argument("--max", type=int, default=8, help="Maximum username length")
    parser.add_argument("--save", action="store_true", help="Save found usernames to file")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--no-banner", action="store_true", help="Do not show ASCII banner")

    args = parser.parse_args()

    if not args.no_banner:
        print(ASCII_BANNER)

    if args.min < 3 or args.max > 16 or args.min > args.max:
        parser.error("Username length must be between 3 and 16.")

    find_usernames(args.count, args.min, args.max, args.save, args.json)

if __name__ == "__main__":
    main()

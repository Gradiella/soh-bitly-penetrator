import requests
import time
import argparse
from enum import Enum
from itertools import permutations, combinations

# ANSI escape codes for coloring the output
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Enum for search radius
class SearchRadius(Enum):
    NEW_ONLY = 1
    OLD = 2
    FULL = 3
    NEWER_ONLY = 4
    MIDDLE = 5
    TRIMMED = 6
    KIMIA = 7
    BC = 8
    PAI = 9
    START = 10
    CA = 11  # Added new search radius
    NEWER_REVISION = 12
    NEW_ONLY_REVISION = 13
    UNTHINKED = 14
    GEO = 15

variable_parts = ["smasoh", "2324"]
bc_parts = ["bc", "kakdika", "2324", "smasoh"]
bc_variants = ["bc", "broadcast", "broadcasting"]
pai_parts = ["pai", "islam", "xi", "11", "andro","ipho"]
geo_parts = ["geografi", "geo", "xi", "11", "andro","ipho"]
ca_parts = ["21ca", "xi", "11"]

# Function to generate all combinations of URLs
def generate_urls(search_radius):
    urls = set()  # Use a set to avoid duplicates
    
    if search_radius in {SearchRadius.OLD, SearchRadius.FULL}:
        for i in range(1, 6):  # s[i] can be 1 to 7
            for j in range(1, 6):  # h[i] can be 1 to 7
                # Base combination
                urls.add(f"http://bit.ly/s{i}-h{j}")
                urls.add(f"http://bit.ly/h{j}-s{i}")
                # With one variable part
                for part in variable_parts:
                    urls.add(f"http://bit.ly/s{i}-h{j}-{part}")
                    urls.add(f"http://bit.ly/h{j}-s{i}-{part}")
                # With both variable parts in different orders
                urls.add(f"http://bit.ly/s{i}-h{j}-{variable_parts[0]}-{variable_parts[1]}")
                urls.add(f"http://bit.ly/s{i}-h{j}-{variable_parts[1]}-{variable_parts[0]}")
                urls.add(f"http://bit.ly/h{j}-s{i}-{variable_parts[0]}-{variable_parts[1]}")
                urls.add(f"http://bit.ly/h{j}-s{i}-{variable_parts[1]}-{variable_parts[0]}")

    if search_radius in {SearchRadius.NEW_ONLY, SearchRadius.FULL}:
        for i in range(1, 6):  # s[i] can be 1 to 7
            for j in range(1, 6):  # h[i] can be 1 to 7
                # With variable parts in different orders
                urls.add(f"http://bit.ly/{variable_parts[0]}-s{i}-h{j}-{variable_parts[1]}")
                urls.add(f"http://bit.ly/{variable_parts[1]}-s{i}-h{j}-{variable_parts[0]}")
                urls.add(f"http://bit.ly/{variable_parts[0]}-s{i}-{variable_parts[1]}-h{j}")
                urls.add(f"http://bit.ly/{variable_parts[1]}-s{i}-{variable_parts[0]}-h{j}")

    if search_radius in {SearchRadius.NEW_ONLY_REVISION, SearchRadius.FULL}:
        for i in range(1, 6):  # s[i] can be 1 to 7
            for j in range(1, 6):  # h[i] can be 1 to 7
                # With variable parts in different orders
                urls.add(f"http://bit.ly/{variable_parts[0]}-h{i}-s{j}-{variable_parts[1]}")
                urls.add(f"http://bit.ly/{variable_parts[1]}-h{i}-s{j}-{variable_parts[0]}")
                urls.add(f"http://bit.ly/{variable_parts[0]}-h{i}-{variable_parts[1]}-s{j}")
                urls.add(f"http://bit.ly/{variable_parts[1]}-h{i}-{variable_parts[0]}-s{j}")

    if search_radius in {SearchRadius.NEWER_ONLY, SearchRadius.FULL}:
        for i in range(1, 6):  # s[i] can be 1 to 7
            for j in range(1, 6):  # h[i] can be 1 to 7
                for part1 in variable_parts:
                    for part2 in variable_parts:
                        if part1 != part2:
                            urls.add(f"http://bit.ly/{part1}-s{i}-{part2}-h{j}")
                            urls.add(f"http://bit.ly/{part1}-s{i}-h{j}-{part2}")
                            urls.add(f"http://bit.ly/s{i}-{part1}-h{j}-{part2}")
                            urls.add(f"http://bit.ly/{part1}-s{i}-{part2}-h{j}")
                            urls.add(f"http://bit.ly/{part1}-s{i}-h{j}-{part2}")
                            urls.add(f"http://bit.ly/s{i}-{part1}-{part2}-h{j}")
    if search_radius in {SearchRadius.NEWER_REVISION, SearchRadius.FULL}:
        for i in range(1, 6):  # s[i] can be 1 to 7
            for j in range(1, 6):  # h[i] can be 1 to 7
                for part1 in variable_parts:
                    for part2 in variable_parts:
                        if part1 != part2:

                            urls.add(f"http://bit.ly/{part1}-h{i}-{part2}-s{j}")
                            urls.add(f"http://bit.ly/{part1}-h{i}-s{j}-{part2}")
                            urls.add(f"http://bit.ly/h{i}-{part1}-s{j}-{part2}")
                            urls.add(f"http://bit.ly/{part1}-h{i}-{part2}-s{j}")
                            urls.add(f"http://bit.ly/{part1}-h{i}-s{j}-{part2}")
                            urls.add(f"http://bit.ly/h{i}-{part1}-{part2}-s{j}")

    if search_radius in {SearchRadius.MIDDLE, SearchRadius.FULL}:
        for i in range(1, 6):  # s[i] can be 1 to 7
            for j in range(1, 6):  # h[i] can be 1 to 7
                for part1 in variable_parts:
                    for part2 in variable_parts:
                        if part1 != part2:
                            urls.add(f"http://bit.ly/s{i}-{part1}-{part2}-h{j}")
                            urls.add(f"http://bit.ly/s{i}-{part1}-h{j}-{part2}")
                            urls.add(f"http://bit.ly/h{i}-{part1}-s{j}-{part2}")
                            urls.add(f"http://bit.ly/h{j}-{part1}-{part2}-s{i}")

    if search_radius == SearchRadius.TRIMMED:
        for i in range(1, 6):  # s[i] can be 1 to 7
            for j in range(1, 6):  # h[i] can be 1 to 7
                # With variable part "2324" in different positions
                urls.add(f"http://bit.ly/h{j}-2324-s{i}")
                urls.add(f"http://bit.ly/s{i}-2324-h{j}")
                urls.add(f"http://bit.ly/2324-s{i}-h{j}")
                urls.add(f"http://bit.ly/2324-h{i}-s{j}")
                # New patterns
                urls.add(f"http://bit.ly/h{i}-smasoh-s{j}")
                urls.add(f"http://bit.ly/s{i}-smasoh-h{j}")
                urls.add(f"http://bit.ly/smasoh-s{i}-h{j}")
                urls.add(f"http://bit.ly/smasoh-h{i}-s{j}")

    if search_radius == SearchRadius.UNTHINKED:
        for i in range(1, 6):  # s[i] can be 1 to 7
            for j in range(1, 6):  # h[i] can be 1 to 7
                for part1 in variable_parts:
                    for part2 in variable_parts:
                        if part1 != part2:
                            urls.add(f"http://bit.ly/{part1}-{part2}-h{i}-s{j}")
                            urls.add(f"http://bit.ly/{part1}-{part2}-s{i}-h{j}")
                

    if search_radius == SearchRadius.KIMIA:
        # Generate all permutations of the kimia_parts
        for r in range(2, len(kimia_parts) + 1):  # r is the length of the combination
            for combo in combinations(kimia_parts, r):
                for perm in permutations(combo):
                    urls.add(f"http://bit.ly/{'-'.join(perm)}andro")

    if search_radius == SearchRadius.BC:
        # Generate all permutations of the bc_parts with bc_variants
        for variant in bc_variants:
            for r in range(2, len(bc_parts) + 1):  # r is the length of the combination
                for combo in combinations(bc_parts, r):
                    if "bc" in combo:
                        combo = tuple(variant if x == "bc" else x for x in combo)
                    for perm in permutations(combo):
                        urls.add(f"http://bit.ly/{'-'.join(perm)}")

    if search_radius == SearchRadius.PAI:
        # Generate all permutations of the pai_parts
        for r in range(2, len(pai_parts) + 1):  # r is the length of the combination
            for combo in combinations(pai_parts, r):
                if "11" in combo and "xi" in combo:
                    continue  # Skip combinations that contain both "pai" and "agama"
                if "pai" in combo and "islam" in combo:
                    continue  # Skip combinations that contain both "pai" and "agama"
                if "andro" in combo and "ipho" in combo:
                    continue  # Skip combinations that contain both "pai" and "agama"
                for perm in permutations(combo):
                    urls.add(f"http://bit.ly/{''.join(perm)}")

    if search_radius == SearchRadius.GEO:
        for r in range(2, len(geo_parts) + 1):
            for combo in combinations(geo_parts, r):
                if "geo" not in combo:
                    continue
                if "11" in combo and "xi" in combo:
                    continue
                if "geo" in combo and "geografi" in combo:
                    continue
                if "andro" in combo and "ipho" in combo:
                    continue
                for perm in permutations(combo):
                    urls.add(f"http://bit.ly/{''.join(perm)}")

    if search_radius == SearchRadius.START:
        for i in range(1, 6):  # s[i] can be 1 to 7
            for j in range(1, 6):  # h[i] can be 1 to 7
                for part in variable_parts:
                    urls.add(f"http://bit.ly/{variable_parts[0]}-s{i}-h{j}")
                    urls.add(f"http://bit.ly/{variable_parts[0]}-h{i}-s{j}")
                    urls.add(f"http://bit.ly/{variable_parts[1]}-s{i}-h{j}")
                    urls.add(f"http://bit.ly/{variable_parts[1]}-h{i}-s{j}")
                    
                    urls.add(f"http://bit.ly/s{i}-h{j}-{variable_parts[0]}")
                    urls.add(f"http://bit.ly/h{i}-s{j}-{variable_parts[0]}")
                    urls.add(f"http://bit.ly/s{i}-h{j}-{variable_parts[1]}")
                    urls.add(f"http://bit.ly/h{i}-s{j}-{variable_parts[1]}")

    if search_radius == SearchRadius.CA:
        # Generate all permutations of the ca_parts
        for r in range(2, len(ca_parts) + 1):  # r is the length of the combination
            for combo in combinations(ca_parts, r):
                if "21ca" not in combo:
                    continue  # Skip combinations that do not contain "21ca"
                for perm in permutations(combo):
                    urls.add(f"http://bit.ly/{''.join(perm)}andro")

    return urls

# Function to normalize a URL by sorting its components
def normalize_url(url):
    parts = url.split('/')
    if len(parts) > 3:
        components = parts[3].split('-')
        components.sort()
        return f"http://{parts[2]}/{'-'.join(components)}"
    return url

# Function to check if a URL is valid
def check_url(url):
    try:
        response = requests.head(url, allow_redirects=True)
        if response.status_code == 200:
            print(f"{GREEN}Valid link: {url}{RESET}")
            return True
        elif response.status_code == 404:
            print(f"{RED}Invalid link (status code {response.status_code}): {url}{RESET}")
            return False
        else:
            print(f"{RED}Rate limited!, please change proxy{RESET}")
            return None
    except requests.RequestException as e:
        print(f"{RED}Error checking {url}: {e}{RESET}")
        return None

# Main function
def main(search_radius):
    urls = generate_urls(search_radius)
    checked_urls = set()  # Set to store checked URLs
    valid_urls = []  # List to store valid URLs

    # Load already leeched URLs from file
    try:
        with open("checked_urls.txt", "r") as checked_file:
            checked_urls = set(line.strip() for line in checked_file)
    except FileNotFoundError:
        pass

    # Open files for writing
    with open("query.txt", "a") as query_file, open("leeched.txt", "a") as leech_file:
        for url in urls:
            normalized_url = normalize_url(url)


            query_file.write(f"{url}\n")
            print(f"Checking URL: {url}")
            result = check_url(url)
            if result is None:
                break
            if result:
                valid_urls.append(url)
                leech_file.write(f"{url}\n")
            checked_urls.add(normalized_url)
    
    # Save checked URLs to file
    with open("checked_urls.txt", "w") as checked_file:
        for checked_url in checked_urls:
            checked_file.write(f"{checked_url}\n")

    # Print all successful links
    if valid_urls:
        print("\nSuccessfully leeched links:")
        for valid_url in valid_urls:
            print(valid_url)
    else:
        print("\nNo valid links found.")

# Set the search radius as needed
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Leech bit.ly links based on search radius.")
    parser.add_argument("search_radius", choices=[e.name for e in SearchRadius], help="Search radius to use for generating URLs.")
    args = parser.parse_args()

    search_radius = SearchRadius[args.search_radius]
    main(search_radius)
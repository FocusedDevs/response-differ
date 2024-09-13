import json
import requests
import argparse
from difflib import unified_diff
from colorama import Fore


def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)


def color_diff(diff):
    for line in diff:
        if line.startswith('+'):
            yield Fore.GREEN + line + Fore.RESET
        elif line.startswith('-'):
            yield Fore.RED + line + Fore.RESET
        elif line.startswith('^'):
            yield Fore.BLUE + line + Fore.RESET
        else:
            yield line


def diff_response(url_a: str, url_b: str):
    print(f'------------------- {url_a} vs. {url_b} -------------------')

    response1 = requests.get(url_a)
    response2 = requests.get(url_b)

    d = unified_diff(
        json.dumps(response1.json(), indent=4, sort_keys=True).splitlines(),
        json.dumps(response2.json(), indent=4, sort_keys=True).splitlines(),
        lineterm=''
    )
    d = color_diff(d)
    print('\n'.join(list(d)))
    print('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser("response-differ")
    parser.add_argument('-u', '--urls', nargs='+', help='<Required> Set flag', required=True)
    args = parser.parse_args()

    urls = args.urls
    if len(urls) % 2 != 0:
        raise Exception('urls must be dividable by 2')

    for a, b in pairwise(urls):
        diff_response(a, b)

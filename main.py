import json
import curlparser
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


def get_json_from_request(url: str) -> list[str]:
    response = requests.get(url)
    if not 'application/json' in response.headers.get('Content-Type', ''):
        raise Exception(f'response header of {url} is not "application/json"')

    return json.dumps(response.json(), indent=4, sort_keys=True).splitlines()


def diff_response(url_a: str, url_b: str):
    print(f'------------------- {url_a} vs. {url_b} -------------------')

    d = unified_diff(
        get_json_from_request(url_a),
        get_json_from_request(url_b),
        lineterm=''
    )
    d = color_diff(d)

    print('\n'.join(list(d)))
    print('\n')


def run_urls(urls: list[str]):
    if len(urls) % 2 != 0:
        raise Exception('urls must be dividable by 2')

    for a, b in pairwise(urls):
        diff_response(a, b)


def run_curl_files(files: list[str]):
    with open(files[0]) as f: curl1 = f.read()
    with open(files[1]) as f: curl2 = f.read()

    request1 = curlparser.parse(curl1)
    request2 = curlparser.parse(curl2)

    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser("response-differ")
    parser.add_argument('-u', '--urls', nargs='+', help='list of URLs you want to compare')
    parser.add_argument('-c', '--curl-files', nargs=2, help='list of 2 files to curl commands')
    args = parser.parse_args()

    if args.urls is not None:
       run_urls(args.urls)
    elif args.curl_files is not None:
        run_curl_files(args.curl_files)

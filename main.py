# ---------------------------------------------------------------------------
# Password Checker
# 2020/11/20
# ---------------------------------------------------------------------------
import requests
import hashlib
import sys


def make_sha1_hash(passwd):
    sha1pass = hashlib.sha1(passwd.encode('utf-8')).hexdigest().upper()
    return sha1pass


def request_api_data(hashed_pass_portion):
    url = 'https://api.pwnedpasswords.com/range/' + hashed_pass_portion
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Fetch Error {res.status_code}: Check API')
    return res


def check_leaks(api_response, hash_tail):
    hashes = (line.split(':') for line in api_response.text.splitlines())
    for h, count in hashes:
        if hash_tail == h:
            return count
    return 0


def main(args):
    with open('tocheck.txt') as pass_file:
        pass_list = pass_file.readlines()
        print(pass_list)
        for passwd in pass_list:
            pass_to_check = passwd.rstrip('\n')
            api_pass_hash = make_sha1_hash(pass_to_check)
            response = request_api_data(api_pass_hash[:5])
            count = check_leaks(response, api_pass_hash[5:])
            if count:
                print(f'Password {pass_to_check} has been hacked {count} times')
            else:
                print(f'Password {pass_to_check} is safe.')
    return 'done'

# ---------------------------------------------------------------------------

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))


# -- EOF --------------------------------------------------------------------

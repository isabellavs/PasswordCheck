# ---------------------------------------------------------------------------
# Password Checker
# 2020/11/20
# ---------------------------------------------------------------------------
import PySimpleGUI as sg
import requests
import hashlib

password = ''

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

# Create a user input window
#sg.theme_previewer() # enable this to see what themes are available.
sg.theme('DarkTeal4')

# All the stuff inside your window.
layout = [  [sg.Text('Check if a password has been hacked')],
            [sg.Text('Enter password to be checked'), sg.InputText('', key='Password', password_char='*')],
            [sg.Checkbox('Show password in response', default=False, key='-SHOW-')],
            [sg.Button('Check'), sg.Button('Quit')] ]

# Create the Window
window = sg.Window('Password Checker', layout, alpha_channel=.5, grab_anywhere=True)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Quit': # if user closes window or clicks cancel
        break

    if values['-SHOW-'] == True:
        password = values['Password']
    else:
        password = 'you entered'

    pass_to_check = values['Password'].rstrip('\n')
    api_pass_hash = make_sha1_hash(pass_to_check)
    response = request_api_data(api_pass_hash[:5])
    count = check_leaks(response, api_pass_hash[5:])

    sg.Popup('The password', password,  'has been hacked', count, 'times', keep_on_top=True, no_titlebar=True)
    window['Password'].Update('')

window.close()

# -- EOF --------------------------------------------------------------------

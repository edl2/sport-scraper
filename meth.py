import requests, re, base64
import subprocess
import inquirer
from bs4 import BeautifulSoup
options = ['nbastreams', 'nflstreams', 'cfbstreams', 'lives-mma-streams-3', 'boxing-streams', 'bjj-streams', 'wwestreams']

questions = [
    inquirer.List('cat',
                  message="Choose category",
                  choices=options,
                  ),
]
catan = inquirer.prompt(questions)
fat = catan['cat']
category = 'https://methstreams.com/' + fat + '/'
response = requests.get(category)
description_regex = r"(?<=<a href=\')(.*)(?=' )"
description = re.findall(description_regex, response.text, re.MULTILINE)
print(description)
questions = [
    inquirer.List('what',
                  message="Choose stream",
                  choices=description,
                  ),
]
answers = inquirer.prompt(questions)
user = answers['what']
if fat == 'nbastreams':
    url = user
else:
    url = 'https://methstreams.com/' + user
video_html = requests.get(url).text
video = BeautifulSoup(video_html, "html.parser")
iframe = video.find("iframe").get("src")
r_iframe = requests.get(iframe).text
atob = re.findall(r'window.atob\("(.+?)"\)', r_iframe)[0]
address=base64.b64decode(atob).decode("utf-8")
mpv = subprocess.Popen(["mpv", address])
mpv.wait()
mpv.kill()
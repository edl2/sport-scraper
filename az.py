import requests
import re
import subprocess
import inquirer

options = ['soccer', 'nfl', 'ncaa', 'boxing', 'nba']

questions = [
    inquirer.List('cat',
                  message="Choose category",
                  choices=options,
                  ),
]
catan = inquirer.prompt(questions)
fat = catan['cat']


url = "http://fabtech.work/category/" + fat
response = requests.get(url)
description_regex = r"<div class=\"entry-feature.*?href=\"(.*?)\""
description = re.findall(description_regex, response.text, re.MULTILINE)



questions = [
    inquirer.List('what',
                  message="Choose stream",
                  choices=description,
                  ),
]
answers = inquirer.prompt(questions)

user = answers['what']


stream = user
r = requests.get(stream).text
m3u8 = re.findall(r"source src=\"(.+?)\"", r)[0]
mpv = subprocess.Popen(["mpv", f"{m3u8}", f"--http-header-fields=Referer: http://fabtech.work/"])
mpv.wait()
mpv.kill()

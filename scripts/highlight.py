import json

import requests
from bs4 import BeautifulSoup


def full_games():
    res = requests.get('https://www.youtube.com/channel/UCBGpG-uiIlxb348HZrEprEA')
    soup = BeautifulSoup(res.content, 'html.parser')
    # print(soup.prettify())
    video_scripts = soup.find_all('script')
    bs_to_string = str(video_scripts[27])
    variable_string = bs_to_string.split('var ytInitialData = ')[1].split(';')[0]
    variable_dict = json.loads(variable_string)
    # print(variable_dict)
    # 開啟檔案
    fp = open("a.json", "a")

    # 寫入 This is a testing! 到檔案
    fp.write(json.dump(variable_dict, fp))

    # 關閉檔案
    fp.close()

full_games()

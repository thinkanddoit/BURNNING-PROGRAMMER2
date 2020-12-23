from flask import Flask
import requests
import json
import pandas as pd

app = Flask (__name__)
dataURL = 'https://coroname.me/getdata'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/getdata')
def getdata():
    res = requests.get(dataURL, verify=False)
    data = res.text
    data = json.loads(data)['data']
    daejeonData = getDaejeonData(data)
    print(daejeonData)

    ret = daejeonData.to_json(force_ascii=False)
    return ret


def getDaejeonData(data):
    df = pd.DataFrame.from_dict(data, orient='columns')
    df = df.loc[df.region == '대전']
    df_arrange = pd.DataFrame(df, columns=['visitedDate', 'latlng', 'address', 'place'])
    new = df_arrange['latlng'].str.split(",", n=1, expand=True)
    df_arrange['lat'] = new[0].str.strip()
    df_arrange['lng'] = new[1].str.strip()
    df_arrange.drop(columns=['latlng'], inplace=True)
    df_arrange = df_arrange.T
    return df_arrange

if __name__ == "__main__":
    app.run()

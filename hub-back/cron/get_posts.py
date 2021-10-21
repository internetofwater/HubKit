import os
import json
import requests
import pandas as pd
from datetime import datetime


def fetch(url: str) -> list:
    res = requests.get(url)
    return json.loads(res.content)


def process(posts: list) -> pd.DataFrame:
    processed = []
    for post in posts:
        processed.append({
            'ID': post['id'],
            'UserID': post['userId'],
            'Title': post['title']
        })
    return pd.DataFrame(processed)


def save(posts: pd.DataFrame, path: str) -> None:
    posts.to_csv(path, index=False)


if __name__ == '__main__':
    posts = fetch(url='https://jsonplaceholder.typicode.com/posts')
    posts = process(posts=posts)
    curr_timestamp = int(datetime.timestamp(datetime.now()))
    path = os.path.abspath(f'/app/cron/{curr_timestamp}.csv')
    save(posts=posts, path=path)

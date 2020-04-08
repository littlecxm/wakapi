#!/usr/bin/python3
import random
import string
import sys
from datetime import datetime, timedelta
from typing import List

import requests

N_PROJECTS = 5
N_PAST_HOURS = 24
UA = 'wakatime/13.0.7 (Linux-4.15.0-91-generic-x86_64-with-glibc2.4) Python3.8.0.final.0 vscode/1.42.1 vscode-wakatime/4.0.0'
LANGUAGES = {
    'Go': 'go',
    'Java': 'java',
    'JavaScript': 'js',
    'Python': 'py'
}


class Heartbeat:
    def __init__(
            self,
            entity: str,
            project: str,
            language: str,
            time: float,
            is_write: bool = True,
            branch: str = 'master',
            type: str = 'file'
    ):
        self.entity: str = entity
        self.project: str = project
        self.language: str = language
        self.time: float = time
        self.is_write: bool = is_write
        self.branch: str = branch
        self.type: str = type
        self.category: str = None


def generate_data(n: int) -> List[Heartbeat]:
    data: List[Heartbeat] = []
    now: datetime = datetime.today()
    projects: List[str] = [randomword(random.randint(5, 10)) for _ in range(5)]
    languages: List[str] = list(LANGUAGES.keys())

    for i in range(n):
        p: str = random.choice(projects)
        l: str = random.choice(languages)
        f: str = randomword(random.randint(2, 8))
        delta: timedelta = timedelta(
            hours=random.randint(0, N_PAST_HOURS - 1),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )

        data.append(Heartbeat(
            entity=f'/home/me/dev/{p}/{f}.{LANGUAGES[l]}',
            project=p,
            language=l,
            time=(now - delta).timestamp()
        ))

    return data


def post_data_sync(data: List[Heartbeat], url: str):
    for h in data:
        r = requests.post(url, json=[h.__dict__], headers={
            'User-Agent': UA
        })
        if r.status_code != 200:
            print(r.text)
            sys.exit(1)


def randomword(length: int) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


if __name__ == '__main__':
    n: int = 10
    url: str = 'http://admin:admin@localhost:3000/api/heartbeat'

    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    if len(sys.argv) > 2:
        url = sys.argv[2]

    data: List[Heartbeat] = generate_data(n)
    post_data_sync(data, url)
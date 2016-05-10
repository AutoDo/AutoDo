# utils.py
# Author: Jun-Ho Kim

import os
import git
import shutil
from celery import Celery

app = Celery('utils', broker='redis://localhost:6379/0')


@app.task
def add(file_name):
    os.mkdir(file_name)


class UtilHandler:

    dir_name = "temp"

    def __init__(self, dir_name):
        self.dir_name = dir_name

    def clone_repository(self, git_url):
        git_url = git_url
        if os.path.isdir(self.dir_name):
            shutil.rmtree(self.dir_name)

        os.mkdir(self.dir_name)

        repo = git.Repo.init(self.dir_name)
        origin = repo.create_remote('origin', git_url)
        origin.fetch()
        origin.pull(origin.refs[0].remote_head)

'''
if __name__ == "__main__":
    # Module Testing
    target_url = "https://github.com/JunoJunho/MathProject"
    handler = UtilHandler()
    handler.clone_repository(git_url=target_url)
'''
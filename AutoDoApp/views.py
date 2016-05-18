

import json
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests


def index(request, access_token=""):
    template = loader.get_template('AutoDoApp/index.html')
    context = {
        'access_token': access_token,
        'client_id': "66c40334092cde4ea3bb",
    }
    return HttpResponse(template.render(context=context, request=request))


def oauth_callback(request):
    code = request.GET['code']
    res = post_json(code)
    git_info = email_auth(res)
    django_db_connect(git_info)
    #create_hook(res)
    get_hook_list(res, git_info)
    #create_pull_request(res, git_info)
    return HttpResponseRedirect(reverse('index', kwargs={'access_token': res}))


def django_db_connect(git_info):
    import sqlite3
    con = sqlite3.connect("AutoDo.db")
    cursor = con.cursor()
    #cursor.execute("CREATE TABLE IF NOT EXISTS AutoDo(Email text, ProjectURL text, RepositoryOwner text)")
    cursor.execute("CREATE TABLE IF NOT EXISTS AutoDo(Email text, ProjectURL text)")

    search_query = "SELECT ProjectURL FROM AutoDo WHERE Email='" + git_info.user_email + "'"
    cursor.execute(search_query)
    data = cursor.fetchall()
    #Insert new user information into AutoDo table
    if len(data) == 0:
        print("New user is comming")
        for item in git_info.url_list:
            query = "INSERT INTO AutoDo VALUES ('" + git_info.user_email + "', '" + item + "')"
            cursor.execute(query)

    cursor.execute("SELECT ProjectURL FROM  AutoDo WHERE Email='" + git_info.user_email + "'")
    list_data = cursor.fetchall()
    con.commit()
    return


def email_auth(access_token):

    new_condition = {"access_token": access_token}
    string = requests.get('https://api.github.com/user/emails', new_condition)
    str_json = string.json()
    email = str_json[0]['email']

    repo_string = requests.get('https://api.github.com/user/repos', new_condition)
    repo_json = repo_string.json()

    git_info = GitHubInfo()
    git_info.email_append(email)
    for item in repo_json:
        git_info.url_append(item['html_url'])
        git_info.owner_append(item['owner']['login'])

    get_hook_list(access_token, git_info)
    return git_info


def get_hook_list(access_token, git_info):
    query_string = 'https://api.github.com/repos'
    new_condition = {"access_token": access_token}
    string = requests.get('https://api.github.com/repos/3kd1000/AutoDo/hooks', new_condition)
    hook_json = string.json()
    print(hook_json)


def post_json(code):
    import json
    import urllib.request

    new_conditions = {"client_id": '66c40334092cde4ea3bb',
                      "client_secret": '24076f838f57319415ed5c5946d59a8bb01ddaa3',
                      "code": code}
    params = json.dumps(new_conditions).encode('utf-8')
    git_api_url = "https://github.com/login/oauth/access_token"
    req = urllib.request.Request(git_api_url, data=params,
                                 headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)

    string = response.read().decode('utf-8')
    print(string)
    access_token = string.lstrip("access_token=")
    access_token = access_token.split("&")[0]
    return access_token


def create_pull_request(access_token, project_url):
    import json
    import urllib.request

    new_conditions = {"title": 'test',
                      "body": 'please pull this request',
                      "head": 'develop',
                      "base": "master"}
    params = json.dumps(new_conditions).encode('utf-8')
    git_api_url = "https://api.github.com/repos/AutoDo/AutoDo/pulls"

    req = urllib.request.Request(git_api_url, params)
    req.add_header("content-type", "application/json")
    req.add_header("authorization", "token " + access_token)
    response = urllib.request.urlopen(req)
    string = response.read().decode('utf-8')
    print(string)
    return 1


def create_hook(access_token):
    import json
    import urllib.request

    new_conditions = {"name": 'web',
                      "active": True,
                      "events": ['push', 'pull_request'],
                      "config": {
                          "url": 'http://143.248.49.134:8000/hook/',
                          "content_type": 'json'}
                      }

    params = json.dumps(new_conditions).encode('utf-8')
    print(params)
    git_api_url = "https://api.github.com/repos/3kd1000/AutoDo/hooks"
    req = urllib.request.Request(git_api_url, params)
    req.add_header("content-type", "application/json")
    req.add_header("authorization", "token " + access_token)
    response = urllib.request.urlopen(req)
    string = response.read().decode('utf-8')
    print(string)
    return 1


@csrf_exempt
def hook_callback(request, *args, **kwargs):
    print("hook here")
    data = request.read().decode('utf-8')
    res = json.loads(data)
    return res['repository']['html_url']


class GitHubInfo:

    def __init__(self):
        self.url_list = []
        self.user_email = ""
        self.owner_list = []

    def url_append(self, project_url):
        self.url_list.append(project_url)

    def email_append(self, user_email):
        self.user_email = user_email

    def owner_append(self, owner_account):
        self.owner_list.append(owner_account)
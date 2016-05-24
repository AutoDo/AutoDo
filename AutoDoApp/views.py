
from django.conf import settings
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import GithubInformation

import requests
import hashlib


def index(request, access_token=""):
    template = loader.get_template('AutoDoApp/index.html')
    context = {
        'access_token': access_token,
        'client_id': settings.GIT_HUB_URL,
    }
    return HttpResponse(template.render(context=context, request=request))


def oauth_callback(request):
    code = request.GET['code']
    res = post_json(code)
    #github_info_parse(res)
    branch_name = "refs/heads/test_branch5"
    create_a_branch(res, branch_name)
    create_file_commit(res, branch_name)
    #create_hook(res)
    #get_hook_list(res, git_info)
    create_pull_request(res, "test_branch5")
    return HttpResponseRedirect(reverse('index', kwargs={'access_token': res}))


def github_info_parse(access_token):
    new_condition = {"access_token": access_token}
    string = requests.get('https://api.github.com/user/emails', new_condition)
    str_json = string.json()
    email = str_json[0]['email']

    repo_string = requests.get('https://api.github.com/user/repos', new_condition)
    repo_json = repo_string.json()

    delete_account = GithubInformation.objects.filter(user_email=email)
    if not delete_account.__len__() == 0:
        delete_account.delete()

    for item in repo_json:
        query_string = item['url'] + '/branches'
        string = requests.get(query_string, new_condition)
        branch_json = string.json()
        for branch_item in branch_json:
            query_string = item['url'] + '/branches/' + branch_item['name']
            string = requests.get(query_string, new_condition)
            single_branch_json = string.json()
            print(single_branch_json)
            for parent_item in single_branch_json['commit']['parents']:
                print(parent_item)
                temp_account = GithubInformation(user_email=email, repository_url=item['html_url']
                                                 , repository_owner=item['owner']['login'],
                                                 repository_head=single_branch_json['name'], repository_base='master'
                                                 , parent_branch_sha=parent_item['sha'],
                                                 tree_sha=single_branch_json['commit']['commit']['tree']['sha'])
                temp_account.save()


def create_a_branch(access_token, branch_name):
    condition = {"access_token": access_token}
    res = requests.get("https://api.github.com/repos/JunoJunho/AutoDoTest/git/refs")  # Variable ##########
    res = res.json()
    b_branch_name = ""
    for item in res:
        if "master" in item["ref"]:
            b_branch_name = item['object']['sha']
            break

    params = {"ref": branch_name,
              "sha": b_branch_name
              }
    requests.post("https://api.github.com/repos/JunoJunho/AutoDoTest/git/refs",  # Variable ############
                  params=condition,
                  json=params)


def create_file_commit(access_token, branch_name):
    import base64
    condition = {"access_token": access_token}
    readme_token = "/contents/README.md"
    url = "https://api.github.com/repos/JunoJunho/AutoDoTest"
    put_url = url + readme_token  # Variable ############

    # 1. Get readme.md
    readme_name = "/readme"
    res = requests.get(url + readme_name,  # Variable ############
                       params=condition)
    res = res.json()
    readme_hash_code = res['sha']
    # Need to be fixed
    replacing_content = base64.standard_b64encode(str.encode("## This is replaced README file.")).decode('utf-8')

    # 2. setting params
    params = {  # This needs to be fixed.
        "message": "This is a test message",
        "committer":{
            "name": "Junho Kim",
            "email": "wnsgh611@gmail.com"
        },
        "content": replacing_content,
        "sha": readme_hash_code,
        "branch": branch_name
    }

    # 3. PUT
    res = requests.put(url=put_url,
                       params=condition,
                       json=params)
    res = res.json()
    print(res['commit']['sha'])


def create_commit(access_token):
    temp_objs = GithubInformation.objects.filter(repository_head__contains="develop")
    for item in temp_objs:
        print(item.parent_branch_sha)


def get_hook_list(access_token, git_info):
    new_condition = {"access_token": access_token}
    string = requests.get(settings.GITHUB_API_URL + '/hooks', new_condition)
    hook_json = string.json()


def post_json(code):
    import json
    import urllib.request

    new_conditions = {"client_id": settings.GITHUB_OAUTH_CLIENT_ID,
                      "client_secret": settings.GITHUB_OAUTH_CLIENT_SECRET,
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


def create_pull_request(access_token, branch_name):
    condition = {"access_token": access_token}
    params = {
        "title": 'test',
        "body": 'please pull this request',
        "head": branch_name,
        "base": "master"
    }
    res = requests.post("https://api.github.com/repos/JunoJunho/AutoDoTest/pulls",
                        params=condition,
                        json=params)
    print(res)


def create_hook(access_token):
    import json
    import urllib.request

    new_conditions = {"name": 'web',
                      "active": True,
                      "events": ['push', 'pull_request'],
                      "config": {
                          "url": settings.GIT_HUB_URL + "/hook/",
                          "content_type": 'json'}
                      }

    params = json.dumps(new_conditions).encode('utf-8')
    print(params)
    git_api_url = settings.GITHUB_API_URL + "/hooks"
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


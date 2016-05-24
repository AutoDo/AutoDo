import json
import os
import sys
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import GithubInformation
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

import requests

DEFAULT_TAG = "python_sample_basic"


def index(request, access_token=""):
    template = loader.get_template('AutoDoApp/index.html')
    context = {
        'access_token': access_token,
        'client_id': "66c40334092cde4ea3bb",
    }
    return HttpResponse(template.render(context=context, request=request))


cloudinary.config(
    cloud_name="sample",
    api_key="787295861461512",
    api_secret="avw_ho8hfzfq7C6x-HmnGiM81ZQ"
)


def oauth_callback(request):
    code = request.GET['code']
    res = post_json(code)
    #github_info_parse(res)
    pwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '\\static\\image\\cloudtest.jpg'
    print(pwd)
    image_upload(pwd)
    print("uploaded")
    #create_hook(res)
    #get_hook_list(res, git_info)
    #create_pull_request(res, git_info)
    return HttpResponseRedirect(reverse('index', kwargs={'access_token': res}))


def image_upload(pwd):
    print("--- Upload a local file")
    response = upload(pwd, tags=DEFAULT_TAG)
    dump_response(response)


def dump_response(response):
    print("Upload response:")
    for key in sorted(response.keys()):
        print("  %s: %s" % (key, response[key]))


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
            for parent_item in single_branch_json['commit']['parents']:
                temp_account = GithubInformation(user_email=email, repository_url=item['html_url']
                                                 , repository_owner=item['owner']['login'],
                                                 repository_head=single_branch_json['name'], repository_base='master'
                                                 , parent_branch_sha=parent_item['sha'],
                                                 tree_sha=single_branch_json['commit']['commit']['tree']['sha'])
                temp_account.save()


def create_commit(access_token):
    temp_objs = GithubInformation.objects.filter(repository_head__contains="develop")
    for item in temp_objs:
        print(item.parent_branch_sha)


def get_hook_list(access_token, git_info):
    query_string = 'https://api.github.com/repos'
    new_condition = {"access_token": access_token}
    string = requests.get('https://api.github.com/repos/3kd1000/AutoDo/hooks', new_condition)
    hook_json = string.json()


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


@csrf_exempt
def hook_callback(request, *args, **kwargs):
    print("hook here")
    data = request.read().decode('utf-8')
    res = json.loads(data)
    return res['repository']['html_url']



from django.conf import settings

import json

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.template import loader
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import GithubInformation
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

from AutoDoApp.models import Project

import os

import requests

'''
    # Usage profile.
    branch_name = "refs/heads/test_branch5"
    #create_a_branch(res, branch_name)
    #create_file_commit(res, branch_name)
    #create_hook(res)
    #get_hook_list(res, git_info)
    #create_pull_request(res, "test_branch5")
'''


def index(request, access_token=""):
    template = loader.get_template('AutoDoApp/index.html')
    context = {
        'access_token': access_token,
        'client_id': settings.GIT_HUB_URL,
    }
    return HttpResponse(template.render(context=context, request=request))


def login(request):
    template = loader.get_template('AutoDoApp/login.html')
    context = {
        'client_id': settings.GIT_HUB_URL
    }
    return HttpResponse(template.render(
        context=context,
        request=request)
    )


def main(request):
    if 'oauth' not in request.session:
        return HttpResponseRedirect(reverse('login'))
    elif not request.session['oauth']:
        return HttpResponseRedirect(reverse('login'))

    template = loader.get_template('AutoDoApp/main.html')
    context = {
        'client_id': settings.GIT_HUB_URL
        }
    return HttpResponse(template.render(
        context=context,
        request=request)
        )


@csrf_exempt
def generate_document(request):
    if request.is_ajax():
        if request.method == "POST":
            _data = request.body.decode('utf-8')
            url = json.loads(_data)
            request.session['git_url'] = url['github_url']
            request.session['project_name'] = "".join(request.session['git_url'].split('/')[-1:])
            from AutoDoApp.Manager import ManagerThread
            m = ManagerThread()
            m.put_request(req=request.session['git_url'])

            import time
            time.sleep(10)  # Temporal time sleep

            # Model code needed.
            create_a_branch(access_token=request.session['oauth'], branch_name="refs/heads/tb1", request=request)
            create_file_commit(request.session['oauth'], "refs/heads/tb1", request)
            create_pull_request(request.session['oauth'], "tb1")
    return JsonResponse({'success': True})


def oauth_callback(request):
    code = request.GET['code']
    res = post_json(code)
    request.session['oauth'] = res  # Adding session
    project_list = github_info_parse(res, request)
    if type(project_list) == int and project_list == -1:
        return HttpResponseRedirect(reverse('login'))
    request.session['project_list'] = project_list

    return HttpResponseRedirect(reverse('main'))


def integration_process(request):
    from AutoDoApp.Manager import ManagerThread
    m = ManagerThread()
    m.put_request(req=request.session['git_url'])

    import time
    time.sleep(10)  # Temporal time sleep

    create_a_branch(access_token=request.session['oauth'], branch_name="refs/heads/tb1")
    create_file_commit(request.session['oauth'], "refs/heads/tb1")
    create_pull_request(request.session['oauth'], "tb1")
    return HttpResponseRedirect(reverse('index', kwargs={'access_token': request.session['oauth']}))


def github_info_parse(access_token, request):
    new_condition = {"access_token": access_token}
    string = requests.get('https://api.github.com/user/emails', new_condition)
    str_json = string.json()
    try:
        email = str_json[0]['email']
        string = requests.get('https://api.github.com/user', new_condition)
        str_json = string.json()
        request.session['user_name'] = str_json['login']

        u = GithubInformation.objects.filter(email=email).first()
        if u is None:
            u = GithubInformation()
            u.email = email
            u.account_ID = request.session['user_name']
            u.save()
    except KeyError:
        return -1
    project_list = []

    repo_string = requests.get('https://api.github.com/user/repos', new_condition)
    repo_json = repo_string.json()

    delete_account = GithubInformation.objects.filter(user_email=email)
    if not delete_account.__len__() == 0:
        delete_account.delete()

    for item in repo_json:
        query_string = item['url'] + '/branches'
        string = requests.get(query_string, new_condition)
        branch_json = string.json()

        print(item['html_url'])
        # for branch_item in branch_json:
        #     query_string = item['url'] + '/branches/' + branch_item['name']
        #     string = requests.get(query_string, new_condition)
        #     single_branch_json = string.json()
        #     print(single_branch_json)
        #     for parent_item in single_branch_json['commit']['parents']:
        #         print(parent_item)
        #         temp_account = GithubInformation(user_email=email, repository_url=item['html_url']
        #                                          , repository_owner=item['owner']['login'],
        #                                          repository_head=single_branch_json['name'], repository_base='master'
        #                                          , parent_branch_sha=parent_item['sha'],
        #                                          tree_sha=single_branch_json['commit']['commit']['tree']['sha'])
        #         temp_account.save()
        temp_dict = {'project_url': str(item['html_url']),
                     'project_name': "".join(str(item['html_url']).split('/')[-1:])}
        project_list.append(temp_dict)

    request.session['email'] = email
    return project_list


def create_a_branch(access_token, branch_name, request):
    condition = {"access_token": access_token}
    res_string = "https://api.github.com/repos/" + request.session['user_name'] \
                 + "/" + request.session['project_name'] + "/git/refs"
    res = requests.get(res_string)
    res = res.json()
    b_branch_name = ""
    for item in res:
        if "master" in item["ref"]:
            b_branch_name = item['object']['sha']
            break

    params = {"ref": branch_name,
              "sha": b_branch_name
              }
    requests.post(res_string, params=condition, json=params)


def create_file_commit(access_token, branch_name, request):
    import base64
    condition = {"access_token": access_token}
    readme_token = "/contents/README.md"
    url = "https://api.github.com/repos/" + request.session['user_name'] + "/" \
          + request.session['project_name']
    put_url = url + readme_token

    # 1. Get readme.md
    readme_name = "/readme"
    res = requests.get(url + readme_name,  # Variable ############
                       params=condition)
    res = res.json()
    print(res)

    readme_hash_code = res['sha']
    # Need to be fixed
    readme_dir = os.path.join(settings.BASE_DIR, "parsing_result")
    readme_dir = os.path.join(readme_dir, request.session['project_name'] + ".md")
    f = open(readme_dir, 'r')
    lines = f.readlines()
    contents = ""
    for line in lines:
        contents += line
    replacing_content = base64.standard_b64encode(str.encode(contents)).decode('utf-8')

    # 2. setting params
    params = {  # This needs to be fixed.
        "message": "This is a test message",
        "committer": {
            "name": request.session['user_name'],
            "email": request.session['email']
        },
        "content": replacing_content,
        "sha": readme_hash_code,
        "branch": branch_name
    }
    print("Put commit")

    # 3. PUT
    res = requests.put(url=put_url,
                       params=condition,
                       json=params)
    print(res)


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
    print("Put PR")
    res = requests.post("https://api.github.com/repos/JunoJunho/AutoDoTestApp/pulls",
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


@csrf_exempt
def hook_callback(request, *args, **kwargs):
    print("hook here")
    data = request.read().decode('utf-8')
    res = json.loads(data)
    return res['repository']['html_url']


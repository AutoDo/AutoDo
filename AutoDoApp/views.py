
from django.conf import settings

import json

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.template import loader
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import User
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
            proj_desc = url['desc']
            from AutoDoApp.Manager import ManagerThread
            m = ManagerThread()
            p = Project.objects.filter(repository_url__exact=request.session['git_url']).first()
            m.put_request(req=request.session['git_url'], desc=proj_desc)

            import time
            time.sleep(10)  # Temporal time sleep

            branch_id = p.branch_count
            autodo_prefix_branch_name = "AutoDo_" + str(branch_id)
            branch_name = "refs/heads/" + autodo_prefix_branch_name
            create_a_branch(access_token=request.session['oauth'],
                            branch_name=branch_name,
                            request=request)
            create_file_commit(request.session['oauth'], branch_name, request)
            create_pull_request(request.session['oauth'], autodo_prefix_branch_name, request)

            # Update branch name
            p.update()
            p.desc_update(proj_desc)
    return HttpResponse(json.dumps({'success': True}), content_type='application/json')


def oauth_callback(request):
    code = request.GET['code']
    res = post_json(code)
    request.session['oauth'] = res  # Adding session
    # params = {
    #     'client_secret': settings.GITHUB_OAUTH_CLIENT_SECRET
    # }
    # condition = {"access_token": res,
    #              "clients": settings.GITHUB_OAUTH_CLIENT_ID}
    # res = requests.put(url='https://api.github.com/authorizations/clients/' + settings.GITHUB_OAUTH_CLIENT_ID,
    #                    params=condition,
    #                    json=params)
    # print(res.json())
    #
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
        print(str_json['login'])
        u = User.objects.filter(email__exact=email).first()
        if u is None:
            u = User(email=email, account_ID=request.session['user_name'])
            # u.access_token = "test_token"
            # u.email = email
            # u.account_ID = request.session['user_name']
            u.save()
    except KeyError:
        print("key_error")
        return -1
    project_list = []

    repo_string = requests.get('https://api.github.com/user/repos', new_condition)
    repo_json = repo_string.json()

    u = User.objects.filter(account_ID__exact=request.session['user_name']).first()

    for item in repo_json:
        # print(item['html_url'])
        p = Project.objects.filter(repository_url__exact=item['html_url']).first()
        p_name = "".join(str(item['html_url']).split('/')[-1:])
        try:
            project_license = item['license']['name']
            print(project_license)
        except KeyError:
            project_license = "No license"

        if p is None:
            p = Project()
            p.repository_url = item['html_url']
            p.repository_owner = item['owner']['login']
            p.description = p_name
            p.user = u
            p.project_license = project_license
            p.save()

        temp_dict = {'project_url': str(item['html_url']),
                     'project_name': p_name,
                     'project_desc': p.description,
                     'project_license': project_license}
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
    res = requests.get(url + readme_name,
                       params=condition)
    res = res.json()

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
        "message": "PR " + branch_name,
        "committer": {
            "name": request.session['user_name'],
            "email": request.session['email']
        },
        "content": replacing_content,
        "sha": readme_hash_code,
        "branch": branch_name
    }

    # 3. PUT
    res = requests.put(url=put_url,
                       params=condition,
                       json=params)


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


def create_pull_request(access_token, branch_name, request):
    condition = {"access_token": access_token}
    params = {
        "title": '[AutoDo] Document generated ' + branch_name,
        "body": 'This is generated by AutoDo system.',
        "head": branch_name,
        "base": "master"
    }
    print("Put PR")
    api_url = "https://api.github.com/repos/" + request.session['user_name'] + "/" \
              + request.session['project_name']
    res = requests.post(api_url + "/pulls",
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
    import json
    import urllib.request
    print("hook here")
    data = request.read().decode('utf-8')
    res = json.loads(data)
    email = res['commits'][0]['author']['email']
    u = User.objects.filter(email__exact=email).first()
    p = Project.objects.filter(repository_url__exact=res['repository']['html_url']).first()
    from AutoDoApp.Manager import ManagerThread
    m = ManagerThread()
    m.put_request(req=res['repository']['html_url'], desc=p.description)

    token = u.access_token

    import time
    time.sleep(10)  # Temporal time sleep
    branch_id = p.branch_count
    autodo_prefix_branch_name = "AutoDo_" + str(branch_id)
    branch_name = "refs/heads/" + autodo_prefix_branch_name
    create_a_branch(access_token=token,
                    branch_name=branch_name,
                    request=request)
    create_file_commit(token, branch_name, request) # OAuth call back token
    create_pull_request(token, autodo_prefix_branch_name, request)
    p.update()
    return HttpResponse(res)


def hook_test(request):
    template = loader.get_template('AutoDoApp/integration_test_page.html')
    context = {
        'client_id': settings.GIT_HUB_URL,
        'client_secret': settings.GITHUB_OAUTH_CLIENT_SECRET
    }

    return HttpResponse(template.render(context=context, request=request))


def hook_process(request):
    params = {
        'client_secret': settings.GITHUB_OAUTH_CLIENT_SECRET
    }
    res = requests.put(url='https://api.github.com/authorizations',
                       json=params)

    print(res.json())

    return HttpResponseRedirect(reverse('hook_test'))



from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


def index(request, access_token = ""):
    template = loader.get_template('AutoDoApp/index.html')

    context = {
        'access_token': access_token,
        'client_id': "17e7ac4cf6fc3a11f04f",
    }
    return HttpResponse(template.render(context=context, request=request))


def oauth_callback(request):
    code = request.GET['code']
    res = post_json(code)
    return HttpResponseRedirect(reverse('index', kwargs={'access_token': res}))


def post_json(code):
    import json
    import urllib.request
    import codecs
    new_conditions = {"client_id": '17e7ac4cf6fc3a11f04f',
                      "client_secret": '51fbf1b3ef08a04ee48680fdac6664cb08aa0071',
                      "code": code}
    params = json.dumps(new_conditions).encode('utf8')
    git_api_url = "https://github.com/login/oauth/access_token"
    req = urllib.request.Request(git_api_url, data=params,
                                 headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)
    #reader = codecs.getreader('utf-8')
    string = response.read().decode('utf-8')
    print(string)
    access_token = string.lstrip("access_token=")
    access_token = access_token.split("&")[0]
    print(access_token)

    return access_token

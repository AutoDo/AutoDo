from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('AutoDoApp/index.html')

    context = {
        'access_token': "This is token",
        'client_id': "17e7ac4cf6fc3a11f04f",
    }
    return HttpResponse(template.render(context=context, request=request))


def oauth_callback(request):
    code = ""
    code = request.GET['code']
    res = post_json(code)
    template = loader.get_template('AutoDoApp/index.html')
    context = {
        'access_token': res,
        'client_id': "17e7ac4cf6fc3a11f04f"
    }
    return HttpResponse(template.render(context=context, request=request))


def post_json(code):
    import json
    import urllib.request

    new_conditions = {"client_id": '17e7ac4cf6fc3a11f04f',
                      "client_secret": '51fbf1b3ef08a04ee48680fdac6664cb08aa0071',
                      "code": code}
    params = json.dumps(new_conditions).encode('utf8')
    git_api_url = "https://github.com/login/oauth/access_token"
    req = urllib.request.Request(git_api_url, data=params,
                                 headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)
    return response

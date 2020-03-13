from importlib import import_module

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from digitalarz.utils import Session_Utils


def home_index(request):
    return render(request, "index.html")


@csrf_exempt
def auth_user(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        user_items = Context_Utils.get_user_items(user)
        navbar_items = Context_Utils.get_navbar_items(user)
        request.session.modified = True
        return JsonResponse(
            {"status": 200, "payload": {
                "user": {
                    "username": user.username,
                    "session_key": request.session.session_key
                },
                "user_items": user_items,
                "nav_items": navbar_items
            }})
    else:
        return JsonResponse({"status": 404, "payload": None})


@csrf_exempt
def unauth_user(request):
    try:
        username = request.POST.get('username', None)
        session_key = request.POST.get('session_key', None)
        if session_key:
            request.session = Session_Utils.get_session(session_key)
            if request.session.session_key == session_key:
                request.user = Session_Utils.get_session_user(session_key)
        logout(request)
        Session_Utils.delete_session_cache(session_key)
        return JsonResponse({"status": 200, "payload": {"message": "User successfully logged out"}})
    except Exception as e:
        return JsonResponse({"status": 404, "payload": {"message": str(e)}})

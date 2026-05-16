# dsite/http/router.py

from dsite.urls import urlpatterns


def resolve(path):

    for route, view in urlpatterns:

        if route == path:
            return view

    return None

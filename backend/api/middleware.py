import jwt
from django.conf import settings
from django.urls import resolve
from django.http import HttpResponseForbidden
secret_key = getattr(settings, 'SECRET_KEY', 'default_value_if_not_set')

class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if request.path.find('/api/users/get') != -1 or request.path.find('/api/transactions/get/all') != -1 or request.path.find('/api/reminders/get/all') != -1:
            response = self.get_response(request)
            User = request.headers['usertoken']
            User = jwt.decode(User, secret_key, algorithms=['HS256'])
            if User['is_superuser']:
                return response
            else:
                return HttpResponseForbidden("You do not have permission to access this resource.")
        elif request.path.find('/api/user/update/') != -1:
            response = self.get_response(request)
            User = request.headers['usertoken']
            User = jwt.decode(User, secret_key, algorithms=['HS256'])
            username = request.headers['username']

            if(User['username'] == username):
                return response
            
            return HttpResponseForbidden("You do not have permission to access this resource.")

        else:
            response = self.get_response(request)
            # response['X-Custom-Header'] = 'Hello from CustomHeaderMiddleware'
        return response

    def process_response(self, request, response):
        print(secret_key)
        response = self.get_response(request)
        response['X-Custom-Header'] = 'Hello from CustomHeaderMiddleware'

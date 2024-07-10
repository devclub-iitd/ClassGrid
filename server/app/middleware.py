import requests

class CheckAuthentication(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        request.kerberos = None

        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION']
            if auth.startswith('Bearer '):
                response = self.send_request(auth.split(' ')[1])
                if response.status_code == 200:
                    request.kerberos = response.json().get('userPrincipalName').split('@')[0]
        
        response = self.get_response(request)

        return response
    
    def send_request(self, access_token):
        options = {
            'headers': {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
                }
        }
        response = requests.get('https://graph.microsoft.com/v1.0/me', **options, timeout=10)
        return response
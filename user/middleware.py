from .models import RequestLog

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        existing = RequestLog.objects.filter(path=request.path, method=request.method).first()
        if existing:
            existing.count += 1
            existing.save()
        else:
            RequestLog.objects.create(path=request.path, method=request.method)

            
        response = self.get_response(request)

        # print("middleware after response")
        # Code to be executed for each request/response after
        # the view is called.


        return response

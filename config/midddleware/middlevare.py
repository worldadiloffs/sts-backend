from django.utils.deprecation import MiddlewareMixin

class MobileDetectionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        request.is_mobile = 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent

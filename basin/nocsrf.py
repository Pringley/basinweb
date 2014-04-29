# NOT FOR PRODUCTION!
class DisableCSRF(object):
    """Middleware to ignore CSRF protection."""
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

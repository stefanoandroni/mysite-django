from django.http import Http404

class HtmxOnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.htmx: 
            raise Http404
        return super().dispatch(request, *args, **kwargs)
from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def navactive(request, urls):
    if request.path in ( reverse(url) for url in urls.split() ):
        return "active"
    return ""

@register.simple_tag
def form_error(err):
    if not err:
        return ""

    if type(err) is list:
        c = ""
        for e in err:
            c += form_error(e)
        return c
    else:
        return """
    <div class="alert alert-danger">
        <button type="button" class="close" data-dismiss="alert">&times;</button>
        <strong>Error</strong> %s
    </div>
    """ % (err,)
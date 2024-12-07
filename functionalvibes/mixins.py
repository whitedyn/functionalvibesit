from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Member


class MemberOnlyMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.session.get('has_privileged_access') == True or request.user.is_staff:
            return super(MemberOnlyMixin, self).dispatch(request, *args, **kwargs)
        else:
            if 'privilege_password' in request.GET:
                # print('request.GET %s ' % request.GET)
                is_member = Member.objects.filter(password=request.GET.get('privilege_password', ''),
                                                  active=True).exists()
                # print('is_member %s' % is_member)
                if is_member:
                    request.session['has_privileged_access'] = True
                    return super(MemberOnlyMixin, self).dispatch(request, *args, **kwargs)
            return HttpResponseRedirect(reverse("password_form_view"))

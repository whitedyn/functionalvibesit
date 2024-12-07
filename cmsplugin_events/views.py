from django.views.generic import ListView, DetailView
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.views.generic.edit import FormView
from datetime import datetime
from .models import Event, Category
from functionalvibes.models import BookEvent
from functionalvibes.forms import BookEventForm

# class EventListView(ListView):
#     model = Event
#
#     # def post(self, request, *args, **kwargs):
#     #     pass
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(EventListView, self).get_context_data(**kwargs)
#
#         context['events'] = Event.objects.filter(event_start__gte=datetime.today())
#
#         return context


class EventListView(FormView):
    model = BookEvent
    # context_object_name = 'team_member'
    template_name = "cmsplugin_events/event_list.html"
    form_class = BookEventForm
    success_url = '/event-request-success/'

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        events = Event.objects.filter(event_start__gte=datetime.today())
        context['events'] = events
        return context

    def form_valid(self, form):
        contact_form = form.save(commit=False)

        name = form.cleaned_data['name']
        phone = form.cleaned_data['phone']
        email = self.request.POST.get('email')# form.cleaned_data['email']
        event = form.cleaned_data['event']
        # if self.request.user.is_authenticated:
        #     contact_form.user = self.request.user
        # contact_form.ip = get_client_ip(self.request)
        # date_created = form.cleaned_data['date_created']
        comments = form.cleaned_data['comments']

        message = 'Full name: %s, ' "\n" \
                  'E-mail: %s,' "\n" \
                  'Telephone: %s,' "\n" \
                  'Event: %s,' "\n" \
                  'Notes: %s,' \
                  % (name, email, phone, event, comments if comments else '')

        subject = 'Event registration for %s (%s)' %(name, event)


        try:
            contact_form.save()
            send_mail(subject, message, email, [settings.EMAIL_RECEIVER]) #fail_silently=False
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return super().form_valid(form)



class EventDetailView(DetailView):
    model = Event
    context_object_name = 'event'
    template_name = "cmsplugin_events/event_detail.html"


class CategoryListView(ListView):
    model = Category

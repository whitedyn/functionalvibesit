from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormMixin, FormView
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from django.shortcuts import redirect
from django.urls import reverse
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from .models import (
    Language,
    TeamMember,
    TestimonialCategories,
    Testimonial,
    MemberVideo,
    HowWeRollPoint,
    Faq, Post,
    Member,
    Service,
    Contact,
    Subscribe,
    GuideQuestionary,
    QuestionaryFreeAssessment,
    QuestionaryReceiveOffer,
    GuideFile
)
from .mixins import MemberOnlyMixin
from django.contrib.auth import authenticate, login, logout
from .forms import ContactForm, BookCoachForm, GuideQuestionaryForm
from .utils import SendSubscribeMail

# from django.utils.crypto import get_random_string
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
import random
import string
from django.middleware.gzip import GZipMiddleware


gzip_middleware = GZipMiddleware()
class TeamList(ListView):
    template_name = "team.html"
    model = TeamMember

    def get_context_data(self, *args, **kwargs):
        context = super(TeamList, self).get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.filter(active=True).order_by('order')
        return context


class ServicesList(ListView):
    template_name = "services.html"
    model = Service

    def get_context_data(self, *args, **kwargs):
        context = super(ServicesList, self).get_context_data(**kwargs)
        context['services'] = Service.objects.filter(active=True).order_by('order')
        return context



class ServiceView(DetailView):
    model = Service
    context_object_name = 'service'
    template_name = "single_service.html"


class Testimonials(ListView):
    template_name = "testimonials.html"
    model = Testimonial

    def get_context_data(self, *args, **kwargs):
        context = super(Testimonials, self).get_context_data(**kwargs)
        context['sliders'] = Testimonial.objects.filter(active=True,
                                                        top_story=True,
                                                        slide__isnull=False).order_by('order')
        context['testimonials'] = Testimonial.objects.filter(active=True).prefetch_related('category')
        context['categories'] = TestimonialCategories.objects.filter(active=True,)
        # top_story=False,.order_by('order')[:5]

        return context


class Jobs(ListView):
    template_name = "jobs.html"
    model = MemberVideo

    # def get_context_data(self, *args, **kwargs):
    #     context = super(Jobs, self).get_context_data(**kwargs)
    #     context['jobs'] = Job.objects.filter(active=True,)  # .order_by('order')
    #
    #     return context


class MemberVideos(MemberOnlyMixin, ListView):
    template_name = "members.html"
    model = MemberVideo

    def get(self, request, *args, **kwargs):
        return redirect('contact')

    def get_context_data(self, *args, **kwargs):
        context = super(MemberVideos, self).get_context_data(**kwargs)
        context['videos'] = MemberVideo.objects.filter(
            active=True,
            display_at__members_area=True,
            display_at__vibes_in_action=False,
        )  # .order_by('order')

        return context


class VibesInAction(ListView):
    template_name = "vibes-in-action.html"
    model = MemberVideo

    def get_context_data(self, *args, **kwargs):
        context = super(VibesInAction, self).get_context_data(**kwargs)
        context['videos'] = MemberVideo.objects.filter(active=True,
                                                       display_at__members_area=False,
                                                       display_at__vibes_in_action=True,
                                                       )  # .order_by('order')

        return context


class VibesInActionVideo(DetailView):
    model = MemberVideo
    context_object_name = 'video'
    template_name = "video_detail.html"
    # pk_url_kwarg = 'spk'
    #
    # def get_queryset(self):
    #    return MemberVideo.objects.filter(id=self.kwargs['pk'],
    #                                      active=True,
    #                                      display_at__members_area=False,
    #                                      display_at__vibes_in_action=True,)

    def get_context_data(self, **kwargs):
        context = super(VibesInActionVideo, self).get_context_data(**kwargs)
        # curr_video = MemberVideo.objects.filter(id=self.kwargs['pk'],
        #                                         active=True,
        #                                         display_at__members_area=False,
        #                                         display_at__vibes_in_action=True)
        # videos = MemberVideo.objects.filter(active=True,
        #                                     display_at__members_area=False,
        #                                     display_at__vibes_in_action=True).exclude(id=self.kwargs['pk'])

        pre_video = MemberVideo.objects.filter(id__lt=self.kwargs['pk'],
                                               active=True,
                                               display_at__members_area=False,
                                               display_at__vibes_in_action=True).first()
        next_video = MemberVideo.objects.filter(id__gt=self.kwargs['pk'],
                                                active=True,
                                                display_at__members_area=False,
                                                display_at__vibes_in_action=True).first()
        # context['videos'] = videos
        context['pre_video'] = pre_video
        context['next_video'] = next_video
        return context


class NoMember(ListView):
    template_name = "no_members.html"
    model = MemberVideo

    def get(self, request, *args, **kwargs):
        # return HttpResponseRedirect('contact')
        return redirect('contact')

    def get_context_data(self, *args, **kwargs):
        context = super(NoMember, self).get_context_data(**kwargs)
        # context['videos'] = MemberVideo.objects.filter(active=True,)  # .order_by('order')

        return context


class HowWeRoll(ListView):
    template_name = "how_we_roll.html"
    model = MemberVideo

    def get_context_data(self, *args, **kwargs):
        context = super(HowWeRoll, self).get_context_data(**kwargs)
        context['points'] = HowWeRollPoint.objects.filter(active=True,)  # .order_by('order')

        return context


class FaqsList(ListView):
    template_name = "faqs.html"
    model = Faq

    def get_context_data(self, *args, **kwargs):
        context = super(FaqsList, self).get_context_data(**kwargs)
        context['faqs'] = Faq.objects.filter(active=True,)  #.order_by('order')
        context['price_list_exists'] = GuideFile.objects.filter(is_price_list=False).exists()

        return context


class BlogList(ListView):
    template_name = "blog/blog-list.html"
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super(BlogList, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(active=True,)  #.order_by('-post_date')
        context['trends'] = Post.objects.filter(active=True,).order_by('-hits')[0:3]

        return context


class PostView(DetailView):
    template_name = "blog/post-detail.html"
    model = Post
    context_object_name = 'post'

    def get_context_data(self, *args, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['trends'] = Post.objects.filter(active=True,).order_by('-hits')[0:5]
        return context


class About(ListView):
    template_name = "how_we_roll.html"
    model = MemberVideo

    def get_context_data(self, *args, **kwargs):
        context = super(About, self).get_context_data(**kwargs)
        context['points'] = HowWeRollPoint.objects.filter(active=True,)  # .order_by('order')

        return context


class ContactView(FormView):
    template_name = 'contact.html'
    model = Contact
    form_class = ContactForm
    success_url = '/contact-success/'

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ContactView, self).get_context_data(**kwargs)
    #     return context

    def form_valid(self, form):
        contact_form = form.save(commit=False)

        subject = form.cleaned_data['subject']
        email = form.cleaned_data['email']
        if self.request.user.is_authenticated:
            contact_form.user = self.request.user
        # contact_form.ip = get_client_ip(self.request)
        message = form.cleaned_data['message']
        try:
            contact_form.save()
            send_mail(subject, message, email, [settings.EMAIL_RECEIVER]) #fail_silently=False
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return super().form_valid(form)


class ContactSuccess(TemplateView):
    template_name = "contact-success.html"



class TeamMemberView(FormView):
    model = TeamMember
    # context_object_name = 'team_member'
    template_name = "team_member.html"
    form_class = BookCoachForm
    success_url = '/coach-book-request/'

    def get_context_data(self, **kwargs):
        context = super(TeamMemberView, self).get_context_data(**kwargs)
        team_member = TeamMember.objects.filter(slug=self.kwargs['slug']).first()
        context['team_member'] = team_member if team_member else None
        return context

    # def post(self, request, *args, **kwargs):
    #     form = BookCoachForm(request.POST)
    #     print('enterred')
    #     coach_email = request.POST.get('team_member_pk', None)
    #     print('coach_email %s' % coach_email)
    #
    #     # form = BookCoachForm(data=request.POST)
    #     # print('form1 %s' % form1)
    #     print('BookCoachForm %s' % BookCoachForm)
    #     # if form.is_valid():
    #     # object = form.save()
    #     form = BookCoachForm(request.POST or None)
    #     # form.save()
    #     # print('request.method %s' % request.method)
    #     if request.method == 'POST':
    #         print('POST')
    #         if form.is_valid:
    #             print('form')
    #             # print('self.cleaned_data %s' % self.request)
    #             # form.save()
    #             # print(object)
    #             # print(form.is_valid)
    #
    #             # print('post request %s' % self.request.post)
    #             # contact_form = form.save(commit=False)
    #             # print(post)
    #             name = request.POST.get('name') #form.cleaned_data['name']
    #             phone = request.POST.get('phone') #form.cleaned_data['phone']
    #             email = request.POST.get('email') #form.cleaned_data['email']
    #             coach = request.POST.get('coach') #form.cleaned_data['coach']
    #             # if self.request.user.is_authenticated:
    #             #     contact_form.user = self.request.user
    #             # contact_form.ip = get_client_ip(self.request)
    #             date_created = request.POST.get('date_created') #form.cleaned_data['date_created']
    #             date_requested = request.POST.get('date_requested') #form.cleaned_data['date_requested']
    #             comments = request.POST.get('comments') #form.cleaned_data['comments']
    #
    #             TeamMember.objects.create()
    #
    #             message = 'Full name: %s, ' "\n" \
    #                       'E-mail: %s,' "\n" \
    #                       'Telephone: %s,' "\n" \
    #                       'Coach: %s,' "\n" \
    #                       'Booking requested for: %s,' "\n" \
    #                       'Notes: %s,' % (name,
    #                                       email,
    #                                       phone,
    #                                       coach,
    #                                       date_requested,
    #                                       comments)
    #
    #             subject = 'Booking request for %s (%s)' % (coach, date_requested)
    #
    #             try:
    #                 # contact_form.save()
    #                 send_mail(subject, message, email, [coach_email, email], fail_silently=False)  #
    #             except BadHeaderError:
    #                 return HttpResponse('Invalid header found.')
    #             return super().post(request, *args, **kwargs)
    #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def form_valid(self, form):
        contact_form = form.save(commit=False)
        coach_email = self.request.POST.get('team_member_pk', None)
        # print(coach_email)

        name = form.cleaned_data['name']
        phone = form.cleaned_data['phone']
        email = self.request.POST.get('email') #form.cleaned_data['email']
        coach = self.request.POST.get('coach') #form.cleaned_data['coach']
        # if self.request.user.is_authenticated:
        #     contact_form.user = self.request.user
        # contact_form.ip = get_client_ip(self.request)
        date_created = self.request.POST.get('date_created') #form.cleaned_data['date_created']
        date_requested = self.request.POST.get('date_requested') #form.cleaned_data['date_requested']
        comments = form.cleaned_data['comments']

        message = 'Full name: %s, ' "\n" \
                  'E-mail: %s,' "\n" \
                  'Telephone: %s,' "\n" \
                  'Coach: %s,' "\n" \
                  'Booking requested for: %s,' "\n" \
                  'Notes: %s' % (name,
                                  email,
                                  phone,
                                  coach,
                                  date_requested,
                                  comments if comments else '')

        subject = 'Booking request for %s (for %s)' %(coach, date_requested)


        try:
            contact_form.save()
            send_mail(subject, message, email, [coach_email], fail_silently=True)
            # send_mail(subject, message, coach_email, [email], fail_silently=True)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return super().form_valid(form)


# class TeamMemberView(DetailView):
#     model = TeamMember
#     context_object_name = 'team_member'
#     template_name = "team_member.html"

    # def get_context_data(self, **kwargs):
    #     context = super(EmailView, self).get_context_data(**kwargs)
    #     team_members = TeamMember.objects.all()
    #     return context


def subscribe(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email_id']
        email_qs = Subscribe.objects.filter(email_id=email)

        if email_qs.exists():
            data = {"status": "404"}
            return JsonResponse(data)
        else:
            Subscribe.objects.create(first_name=first_name, last_name=last_name, email_id=email)
            SendSubscribeMail(email)  # Send the Mail, Class available in utils.py

    # return HttpResponse("/")
    return redirect('/')


class GuideQuestionaryView(FormView):
    template_name = 'guide-questionary.html'
    model = GuideQuestionary
    form_class = GuideQuestionaryForm
    # success_url = reverse_lazy('downloadable_file')

    def get_success_url(self):
        return reverse('downloadable_file')

    def get_context_data(self, *args, **kwargs):
        context = super(GuideQuestionaryView, self).get_context_data(**kwargs)

        context['free_assements'] = QuestionaryFreeAssessment.objects.all()
        context['receive_offers'] = QuestionaryReceiveOffer.objects.all()

        return context

    def form_valid(self, form):
        contact_form = form.save(commit=False)

        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        phone_number = form.cleaned_data['phone_number']
        maximize_effectiveness_of_my_training = form.cleaned_data['maximize_effectiveness_of_my_training']
        get_back_in_shape = form.cleaned_data['get_back_in_shape']
        learn_how_to_exercise_on_my_own = form.cleaned_data['learn_how_to_exercise_on_my_own']
        need_motivation_and_accountability = form.cleaned_data['need_motivation_and_accountability']
        have_a_specific_injury_or_condition = form.cleaned_data['have_a_specific_injury_or_condition']
        have_a_specific_goal_sport_or_event = form.cleaned_data['have_a_specific_goal_sport_or_event']
        want_supervision_and_support = form.cleaned_data['want_supervision_and_support']
        get_a_free_assessment = form.cleaned_data['get_a_free_assessment']
        receive_an_offer = form.cleaned_data['receive_an_offer']
        agree_to_receive_other_communications = form.cleaned_data['agree_to_receive_other_communications']

        if self.request.user.is_authenticated:
            contact_form.user = self.request.user

        message = 'First name: %s, ' "\n" \
                  'Last name: %s, ' "\n" \
                  'E-mail: %s, ' "\n" \
                  'Telephone: %s, ' "\n" \
                  'Maximize effectiveness of my training: %s, ' "\n" \
                  'Get back in shape: %s, ' "\n" \
                  'Learn how to exercise on my own: %s, ' "\n" \
                  'Need motivation and accountability: %s, ' "\n" \
                  'Have a specific injury or condition: %s, ' "\n" \
                  'Have a specific goal (sport or event): %s, ' "\n" \
                  'Want supervision and support: %s, ' "\n" \
                  'Would you like to get a free assessment?: %s, ' "\n" \
                  'Do you want to receive an offer?: %s, ' "\n" \
                  'Agree to receive other communications from Functional Vibes SRL: %s.' "\n" % (first_name,
                                  last_name,
                                  email,
                                  phone_number,
                                  'Yes' if maximize_effectiveness_of_my_training else 'No',
                                  'Yes' if get_back_in_shape else 'No',
                                  'Yes' if learn_how_to_exercise_on_my_own else 'No',
                                  'Yes' if need_motivation_and_accountability else 'No',
                                  'Yes' if have_a_specific_injury_or_condition else 'No',
                                  'Yes' if have_a_specific_goal_sport_or_event else 'No',
                                  'Yes' if want_supervision_and_support else 'No',
                                  get_a_free_assessment,
                                  receive_an_offer,
                                  'Yes' if agree_to_receive_other_communications else 'No'
                                 )
        subject = 'FV questionary from %s %s' %(first_name, last_name)

        try:
            contact_form.save()
            send_mail(subject, message, first_name + ' ' + last_name + '<'+ email + '>', [settings.TEMP_EMAIL_RECEIVER]) #fail_silently=False

            message_html_template = "emails/guide_download.html"
            message_txt_template = "emails/guide_download.txt"
            context = {
                'order': 'file link to be downloaded',
                'email': email,
                'first_name': first_name,
            }
            client_message = render_to_string(message_html_template, context)
            # staff_message = render_to_string(message_txt_template, context)

            # send_mail(
            #     subject=subject,
            #     message=staff_message,
            #     html_message=staff_message,
            #     from_email=email,
            #     recipient_list=[settings.TEMP_EMAIL_RECEIVER],
            #     fail_silently=True
            # )

            send_mail(
                subject=subject,
                message=client_message,
                html_message=client_message,
                from_email="Functional Vibes <info@functionalvibes.com>",
                recipient_list=[email],
                fail_silently=True
            )
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return super(GuideQuestionaryView, self).form_valid(form)


class GuideQuestionarySuccess(TemplateView):
    template_name = "contact-success.html"


def downloadable_file(request):
    file_to_download = GuideFile.objects.filter(is_price_list=False).last()
    fs = FileSystemStorage('media')
    response = FileResponse(fs.open(str(file_to_download.downloadable_file), 'rb'),
                            content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % file_to_download.downloadable_file.url[26:]

    # unique_id = ''
    # random_str = string.ascii_lowercase
    # unique_id = ''.join(random.choice(random_str) for i in range(32))
    # print('unique_id %s' % unique_id)

    return response
    # return redirect('guide_questionary_success')


def price_list_file(request):
    file_to_download = GuideFile.objects.filter(is_price_list=True).last()
    fs = FileSystemStorage('media')
    response = FileResponse(fs.open(str(file_to_download.downloadable_file), 'rb'),
                            content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % file_to_download.downloadable_file.url[26:]

    # unique_id = ''
    # random_str = string.ascii_lowercase
    # unique_id = ''.join(random.choice(random_str) for i in range(32))
    # print('unique_id %s' % unique_id)

    return response
    # return redirect('guide_questionary_success')


def get_price_list(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email_id']
        email_qs = Subscribe.objects.filter(email_id=email)

        if email_qs.exists():
            data = {"status": "404"}
            return JsonResponse(data)
        else:
            Subscribe.objects.create(first_name=first_name, last_name=last_name, email_id=email)
            SendSubscribeMail(email)  # Send the Mail, Class available in utils.py

    # return HttpResponse("/")
    if GuideFile.objects.filter(is_price_list=True).last():
        return redirect('price_list_file')
    else:
        return redirect('/')

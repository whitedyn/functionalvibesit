from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from autoslug import AutoSlugField
from django.utils import timezone


class Language(models.Model):
    name = models.CharField(max_length=120)
    abbreviation = models.CharField(max_length=120, null=True, blank=True)
    icon = models.ImageField(upload_to='images/languages', null=True)

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return self.name


class Slide(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=120)
    order = models.IntegerField(default=0)

    photo = models.ImageField(
        upload_to='slides',
        help_text='width 2400px, height 1100px'
    )

    subtitle = models.CharField(max_length=240, blank=True, null=True)

    button_text = models.CharField(max_length=120, blank=True, null=True)
    button_link = models.CharField(max_length=220, blank=True, null=True)

    second_button_text = models.CharField(max_length=120, blank=True, null=True)
    second_button_link = models.CharField(max_length=220, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Slides'


class Service(models.Model):
    title = models.CharField(max_length=120)
    slug = AutoSlugField(populate_from='title', editable=True, null=True, blank=True)
    order = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    subtitle = models.CharField(max_length=120, null=True, blank=True)
    photo = models.ImageField(upload_to='images/services', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=120, null=True, blank=True)
    telephone = models.CharField(max_length=120, null=True, blank=True)
    custom_read_more_link = models.CharField(max_length=320, null=True, blank=True)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    name = models.CharField(max_length=120)
    # slug = models.SlugField(max_length=125)
    slug = AutoSlugField(populate_from='name', editable=True, null=True, blank=True)
    order = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    position = models.CharField(max_length=120, null=True, blank=True)
    photo = models.ImageField(upload_to='images/team', null=True, blank=True)
    language = models.ManyToManyField(Language, blank=True)
    description = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=120, null=True, blank=True)
    telephone = models.CharField(max_length=120, null=True, blank=True)
    facebook = models.CharField(max_length=120, null=True, blank=True)
    twitter = models.CharField(max_length=120, null=True, blank=True)
    linkedin = models.CharField(max_length=120, null=True, blank=True)
    instagram = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        verbose_name = 'Team member'
        verbose_name_plural = 'Team members'

    def __str__(self):
        return self.name


class TestimonialCategories(models.Model):
    name = models.CharField(max_length=320)
    order = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Testimonial category'
        verbose_name_plural = 'Testimonial categories'

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    title = models.CharField(max_length=320)
    order = models.IntegerField()
    category = models.ManyToManyField(TestimonialCategories,)
    subtitle = models.CharField(max_length=550, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    top_story = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    slide = models.ImageField(upload_to='images/reviews', null=True, blank=True)
    reviewer = models.CharField(max_length=150, blank=True, null=True)
    photo = models.ImageField(upload_to='images/reviewer', null=True, blank=True)
    stars = models.IntegerField(blank=True, null=True, help_text='From 1 to 5 stars rating if needed')

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'

    def __str__(self):
        return self.title


class Member(models.Model):
    name = models.CharField(max_length=320)
    active = models.BooleanField(default=True)
    email_address = models.CharField(max_length=150, blank=True, null=True)
    password = models.CharField(max_length=150, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Member'
        verbose_name_plural = 'Member'

    def __str__(self):
        return self.name


class MemberVideoArea(models.Model):
    vibes_in_action = models.BooleanField(default=False)
    members_area = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Video area'
        verbose_name_plural = 'Video areas'
        unique_together = ['vibes_in_action', 'members_area']

    def __str__(self):
        return 'Vibes_in_action' if self.vibes_in_action else 'Members_area'

class MemberVideo(models.Model):
    title = models.CharField(max_length=320)
    active = models.BooleanField(default=True)
    order = models.IntegerField(blank=True, null=True)
    display_at = models.ForeignKey(MemberVideoArea, null=True, on_delete=models.SET_NULL)
    subtitle = models.CharField(max_length=550, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    vimeo = models.CharField(max_length=550, blank=True, null=True)
    youtube = models.CharField(max_length=550, blank=True, null=True)

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    def __str__(self):
        return self.title


class HowWeRollPoint(models.Model):
    order = models.IntegerField(blank=True, null=True)
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=320)
    subtitle = models.CharField(max_length=550, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/how_we_roll', null=True, blank=True)

    class Meta:
        verbose_name = 'How We Roll Point'
        verbose_name_plural = 'How We Roll Points'

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=150)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             blank=True, null=True,
                             on_delete=models.CASCADE)
    # user = models.ForeignKey(get_user_model(), blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=80, blank=True, null=True)
    phone = models.CharField(max_length=18, blank=True, null=True)
    message = models.TextField(max_length=1020)
    date = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = '01 Contact request'
        verbose_name_plural = '01 Contact requests'

    def __str__(self):
        return self.name


class BookCoach(models.Model):
    name = models.CharField(max_length=150)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             blank=True, null=True,
                             on_delete=models.CASCADE)
    # user = models.ForeignKey(get_user_model(), blank=True, null=True)
    phone = models.CharField(max_length=18, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    coach = models.CharField(max_length=80, blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True, blank=True)
    date_requested = models.DateTimeField(auto_now=True, blank=True)
    comments = models.TextField(max_length=1020, blank=True, null=True)

    class Meta:
        verbose_name = '02 Coach request'
        verbose_name_plural = '02 Coach request'

    def __str__(self):
        return self.name


class BookEvent(models.Model):
    date_created = models.DateTimeField(auto_now=True, blank=True)
    name = models.CharField(max_length=150)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             blank=True, null=True,
                             on_delete=models.CASCADE)
    # user = models.ForeignKey(get_user_model(), blank=True, null=True)
    phone = models.CharField(max_length=18, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    event = models.CharField(max_length=80, blank=True, null=True)
    comments = models.TextField(max_length=1020, blank=True, null=True)

    class Meta:
        verbose_name = '03 event participation'
        verbose_name_plural = '03 event participations'

    def __str__(self):
        return '%s (%s)' %(self.event, self.name)


class Subscribe(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email_id = models.EmailField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s %s (%s)' %(self.first_name, self.last_name, self.email_id)


class QuestionaryFreeAssessment(models.Model):
    option = models.CharField(max_length=250)

    def __str__(self):
        return self.option


class QuestionaryReceiveOffer(models.Model):
    option = models.CharField(max_length=250)

    def __str__(self):
        return self.option


class GuideFile(models.Model):
    name = models.CharField(max_length=250)
    is_price_list = models.BooleanField(default=False)
    downloadable_file = models.FileField(upload_to='downloadable_files')

    def __str__(self):
        return self.name


class Faq(models.Model):
    active = models.BooleanField(default=True)
    order = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=250)
    body = models.TextField()

    class Meta:
        ordering = ['order', '-id', 'title']

    def __str__(self):
        custom_order = ('(' + str(self.order) + ')') if self.order else None
        return f'{str(self.id)} {custom_order}'


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("title"))
    # slug = models.SlugField()
    slug = AutoSlugField(populate_from='title', editable=True)
    active = models.BooleanField(default=True)
    photo = models.ImageField(upload_to='blog')
    hits = models.IntegerField(default=0)
    body = models.TextField(verbose_name=_("Post body"))

    post_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("post date"))
    modified = models.DateTimeField(null=True, blank=True, verbose_name=_("modified"))
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("posted by"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ['-post_date']
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    def __str__(self):
        return self.title

    def post_photo(self):
        if self.photo:
            return self.photo.url
        else:
            return "/media/images/logo.webp"

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug,
        }

        return reverse('post_detail', kwargs=kwargs)


class GuideQuestionary(models.Model):
    submitted = models.DateTimeField(auto_now_add=True, null=True)
    source = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=18, blank=True, null=True)

    maximize_effectiveness_of_my_training = models.BooleanField(default=False)
    get_back_in_shape = models.BooleanField(default=False)
    learn_how_to_exercise_on_my_own = models.BooleanField(default=False)
    need_motivation_and_accountability = models.BooleanField(default=False)
    have_a_specific_injury_or_condition = models.BooleanField(default=False)
    have_a_specific_goal_sport_or_event = models.BooleanField(default=False)
    want_supervision_and_support = models.BooleanField(default=False)

    get_a_free_assessment = models.ForeignKey(QuestionaryFreeAssessment, null=True, on_delete=models.SET_NULL)
    receive_an_offer = models.ForeignKey(QuestionaryReceiveOffer, null=True, on_delete=models.SET_NULL)

    agree_to_receive_other_communications = models.BooleanField(default=False)

    class Meta:
        verbose_name = '04 Questionary'
        verbose_name_plural = '04 Questionaries'

    def __str__(self):
        return '%s (%s)' %(self.first_name, self.last_name)
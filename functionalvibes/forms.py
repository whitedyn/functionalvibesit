from django import forms
from nocaptcha_recaptcha.fields import NoReCaptchaField
from .models import Contact, BookCoach, BookEvent, GuideQuestionary
from django.contrib.auth.models import User
# from PIL import Image


class ContactForm(forms.ModelForm):
    captcha = NoReCaptchaField()
    # name = forms.CharField(
    #     max_length=130,
    #     widget=forms.TextInput(
    #         attrs={
    #             'style': 'border-color: blue;',
    #             'placeholder': 'Write your name here'
    #         }
    #     )
    # )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ContactForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Contact
        # fields = ("name", "email", "mobile", "message")
        fields = '__all__'

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        # ip = cleaned_data.get('ip')
        user = cleaned_data.get('user')
        subject = cleaned_data.get('subject')
        message = cleaned_data.get('message')
        if not message:
            raise forms.ValidationError('You have to write something!')


class BookCoachForm(forms.ModelForm):
    # captcha = NoReCaptchaField()
    # name = forms.CharField(
    #     max_length=130,
    #     widget=forms.TextInput(
    #         attrs={
    #             'style': 'border-color: blue;',
    #             'placeholder': 'Write your name here'
    #         }
    #     )
    # )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(BookCoachForm, self).__init__(*args, **kwargs)

    class Meta:
        model = BookCoach
        # fields = ("name", "email", "mobile", "message")
        fields = '__all__'

    def clean(self):
        cleaned_data = super(BookCoachForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        # ip = cleaned_data.get('ip')
        # user = cleaned_data.get('user')
        coach = cleaned_data.get('coach')
        comments = cleaned_data.get('message')
        date_created = cleaned_data.get('date_created')
        date_requested = cleaned_data.get('date_requested')
        # if not date_requested:
        #     raise forms.ValidationError('You need to select a date and time of the appointment!')


class BookEventForm(forms.ModelForm):
    # captcha = NoReCaptchaField()

    # name = forms.CharField(
    #     max_length=130,
    #     widget=forms.TextInput(
    #         attrs={
    #             'style': 'border-color: blue;',
    #             'placeholder': 'Write your name here'
    #         }
    #     )
    # )

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     super(BookEventForm, self).__init__(*args, **kwargs)

    class Meta:
        model = BookEvent
        fields = '__all__'

    def clean(self):
        cleaned_data = super(BookEventForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        # ip = cleaned_data.get('ip')
        # user = cleaned_data.get('user')
        event = cleaned_data.get('subject')
        comments = cleaned_data.get('message')
        date_created = cleaned_data.get('date_created')
        # if not event:
        #     raise forms.ValidationError('You need to select an event!')


class GuideQuestionaryForm(forms.ModelForm):
    # captcha = NoReCaptchaField()

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     super(GuideQuestionaryForm, self).__init__(*args, **kwargs)

    class Meta:
        model = GuideQuestionary
        fields = '__all__'

    def clean(self):
        cleaned_data = super(GuideQuestionaryForm, self).clean()

        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        email = cleaned_data.get('email')
        phone_number = cleaned_data.get('phone_number')

        maximize_effectiveness_of_my_training = cleaned_data.get('maximize_effectiveness_of_my_training')
        get_back_in_shape = cleaned_data.get('get_back_in_shape')
        learn_how_to_exercise_on_my_own = cleaned_data.get('learn_how_to_exercise_on_my_own')
        need_motivation_and_accountability = cleaned_data.get('need_motivation_and_accountability')
        have_a_specific_injury_or_condition = cleaned_data.get('have_a_specific_injury_or_condition')
        have_a_specific_goal_sport_or_event = cleaned_data.get('have_a_specific_goal_sport_or_event')
        want_supervision_and_support = cleaned_data.get('want_supervision_and_support')

        get_a_free_assessment = cleaned_data.get('get_a_free_assessment')
        receive_an_offer = cleaned_data.get('receive_an_offer')

        agree_to_receive_other_communications = cleaned_data.get('agree_to_receive_other_communications')

        if not (maximize_effectiveness_of_my_training or get_back_in_shape or learn_how_to_exercise_on_my_own
                or need_motivation_and_accountability or have_a_specific_injury_or_condition or
                have_a_specific_goal_sport_or_event or want_supervision_and_support):
            raise forms.ValidationError('Please select one of the downloading reasons!')


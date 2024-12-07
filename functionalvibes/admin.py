from django.contrib import admin
from .models import (
    Language,
    Slide,
    TeamMember,
    TestimonialCategories,
    Testimonial,
    MemberVideo,
    Member,
    HowWeRollPoint,
    Service,
    MemberVideoArea,
    Faq, Post,

    # Forms
    Contact,
    BookCoach,
    BookEvent,

    # GUIDE
    Subscribe, QuestionaryFreeAssessment, QuestionaryReceiveOffer, GuideQuestionary, GuideFile
)
from django.contrib.auth.admin import UserAdmin
from django_summernote.admin import SummernoteModelAdmin
# from .models import User


class MemberVideoAreaAdmin(admin.ModelAdmin):
    list_display = ('vibes_in_action', 'members_area', )


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'position', 'photo', 'active')


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'abbreviation', 'icon')


class TestimonialCategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'active')


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'top_story', 'active', 'photo')
    list_filter = ('top_story', 'active')


class MemberVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'active')


class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'email_address')


class HowWeRollPointAdmin(admin.ModelAdmin):
    list_display = ('order', 'active', 'title', 'image')


# class ServiceAdmin(admin.ModelAdmin):
#     list_display = ('title', 'active', 'slug', 'order')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'date')


class BookCoachAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'coach', 'date_created', 'date_requested')


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email_id', 'timestamp')
    search_fields = ('first_name', 'last_name', 'email_id')


class BookEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'event', 'date_created')

class SlideAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'order', 'photo')


class GuideQuestionaryAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'submitted',
        'agree_to_receive_other_communications'
    )


class blogadmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'active', 'post_date')
    list_filter = ("active",)
    search_fields = ['title',]
    # prepopulating slug from title
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('body',)


class FaqAdmin(SummernoteModelAdmin):
    list_display = ('title', 'active', 'order')
    list_filter = ("active",)
    search_fields = ['title',]
    # prepopulating slug from title
    summernote_fields = ('body',)


class ServiceAdmin(SummernoteModelAdmin):
    list_display = ('title', 'active', 'slug', 'order')
    list_filter = ("active",)
    search_fields = ['title',]
    # prepopulating slug from title
    summernote_fields = ('description',)


admin.site.register(MemberVideoArea, MemberVideoAreaAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(TestimonialCategories, TestimonialCategoriesAdmin)
admin.site.register(Testimonial, TestimonialAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(MemberVideo, MemberVideoAdmin)
admin.site.register(HowWeRollPoint, HowWeRollPointAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(BookCoach, BookCoachAdmin)
admin.site.register(BookEvent, BookEventAdmin)
# admin.site.register(QuestionaryFreeAssessment)
# admin.site.register(QuestionaryReceiveOffer)
admin.site.register(GuideFile)
admin.site.register(Subscribe, SubscribeAdmin)
admin.site.register(Faq, FaqAdmin)
admin.site.register(GuideQuestionary, GuideQuestionaryAdmin)
admin.site.register(Post, blogadmin)
admin.site.register(Slide, SlideAdmin)

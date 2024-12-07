# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import include, url
from django.urls import path, re_path  # include
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from .views import (
    TeamList,
    Testimonials,
    MemberVideos,
    VibesInAction,
    VibesInActionVideo,
    Jobs,
    HowWeRoll,
    FaqsList,
    BlogList, PostView,
    NoMember,
    TeamMemberView,
    ServicesList,
    ServiceView,
    ContactView,
    ContactSuccess,

    subscribe,
    GuideQuestionaryView,
    GuideQuestionarySuccess,
    downloadable_file, price_list_file, get_price_list
)


admin.autodiscover()

urlpatterns = [
    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^team/', TeamList.as_view(), name='team'),
    url(r'^contact/', ContactView.as_view(), name='contact'),
    url(r'^contact-success/', ContactSuccess.as_view(), name='contact_success'),

    url(r'^subscribe/', subscribe, name="subscribe"),
    url(r'^get-price-list/', get_price_list, name="get_price_list"),
    url(r'^guide-questionary/', GuideQuestionaryView.as_view(), name='guide_questionary'),
    url(r'^guide-questionary-success/', GuideQuestionarySuccess.as_view(), name='guide_questionary_success'),
    # url(r'^', downloadable_file, name="downloadable_file"),
    # url(r'^downloadable_file/(?P<unique_id>[-\w]+)/$', downloadable_file, name="downloadable_file"),
    url(r'^downloadable_file/$', downloadable_file, name="downloadable_file"),
    url(r'^price_list_file/$', price_list_file, name="price_list_file"),

    url(r'^coach-book-request/', ContactSuccess.as_view(), name='coach_book_request'),
    url(r'^event-request-success/', ContactSuccess.as_view(), name='event_request_success'),
    url(r'^testimonials/', Testimonials.as_view(), name='testimonials'),
    url(r'^services', ServicesList.as_view(), name='services'),
    url(r'^service/(?P<slug>[-\w]+)/$', ServiceView.as_view(), name='single_service'),
    url(r'^jobs/', Jobs.as_view(), name='jobs'),
    url(r'^members/', MemberVideos.as_view(), name='members'),
    # url(r'^vibes-in-action/', VibesInAction.as_view(), name='vibes_in_action'),
    # url(r'^vibes-video/(?P<pk>\d+)/$', VibesInActionVideo.as_view(), name='vibes_video_detail'),
    url(r'^vibes-video/(?P<pk>\d+)/$', VibesInActionVideo.as_view(), name='vibes_video_detail'),
    url(r'^member/(?P<slug>[-\w]+)/$', TeamMemberView.as_view(), name='team_member'),
    url(r'^how-we-roll/', HowWeRoll.as_view(), name='how_we_roll'),
    url(r'^faq/', FaqsList.as_view(), name='faqs_list'),
    url(r'^blog/', BlogList.as_view(), name='blog_list'),
    path('article/<str:slug>', PostView.as_view(), name='post_detail'),
    url(r'^member-login', NoMember.as_view(), name='password_form_view'),
    url(r'^events/', include(('cmsplugin_events.urls', 'calendar'), namespace='events')),
    url(r'^8sdimkl9/', admin.site.urls),  # NOQA
    path('editor/', include('django_summernote.urls')),
    url(r'^', include('cms.urls')),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
] + staticfiles_urlpatterns()

# urlpatterns += i18n_patterns(
#     url(r'^admin/', admin.site.urls),  # NOQA
#     url(r'^', include('cms.urls')),
# )

# This is only needed when using runserver.
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        # url(r'^media/(?P<path>.*)$', serve,
        #     {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        ] + staticfiles_urlpatterns() + urlpatterns

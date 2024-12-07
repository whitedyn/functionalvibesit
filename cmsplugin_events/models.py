from datetime import datetime

from django.db import models
from django.utils.translation import ugettext as _
from filer.fields.image import FilerImageField

from model_utils.models import TimeStampedModel


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name if self.name else 'Category'

    class Meta:
        verbose_name_plural = 'Categories'


class CurrentEventManager(models.Manager):

    def get_queryset(self):
        return super(CurrentEventManager, self).get_queryset().filter(event_end__gt=datetime.now())


class Event(TimeStampedModel):
    title = models.CharField(_('Title'), max_length=50)
    description = models.TextField(_('Description'))
    event_start = models.DateTimeField(_('Start time'), blank=True)
    event_end = models.DateTimeField(_('End time'), blank=True)
    location = models.CharField(_('Location'), max_length=50, null=True, blank=True)
    image = FilerImageField(null=True, blank=True, default=None, verbose_name=_("Image"), on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    facebook_url = models.URLField(_('Facebook link'), null=True, blank=True)

    objects = models.Manager()
    ongoing = CurrentEventManager()

    class Meta:
        ordering = ['event_start']

    # @models.permalink
    def get_absolute_url(self):
        return 'event_details', (), {'pk': self.pk}

    def __str__(self):
        return self.title 

try:
    from cms.models import CMSPlugin
except ImportError:
    pass
else:
    class EventListPlugin(CMSPlugin):
        title = models.CharField(_('Title'), max_length=50)
        category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

        def __str__(self):
            return self.category.name if self.category else _('All events')

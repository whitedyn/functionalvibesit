from django.utils.translation import gettext as _

from cms.models import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Testimonial, Slide


@plugin_pool.register_plugin   # register the plugin
class TestimonialPlugin(CMSPluginBase):
    model = CMSPlugin  # model where plugin data are saved
    module = _("Testimonials")
    name = _("Testimonials Carousel")
    render_template = "plugins/testimonials_carousel_plugin.html"

    def render(self, context, instance, placeholder):
        testimonials = Testimonial.objects.filter(
            top_story=True, active=True, photo__isnull=False
        )#[:4]
        context.update({
            'instance': instance,
            'testimonials': testimonials,
        })
        return context


@plugin_pool.register_plugin  # register the plugin
class SlidePlugin(CMSPluginBase):
    model = CMSPlugin  # model where plugin data are saved
    module = _("Slides")
    name = _("Home Slides Carousel")  # name of the plugin in the interface
    render_template = "plugins/slides_carousel_plugin.html"

    def render(self, context, instance, placeholder):
        slides = Slide.objects.filter(
            active=True, photo__isnull=False
        ).order_by('order')[:8]
        context.update({
            'instance': instance,
            'slides': slides,
        })
        return context


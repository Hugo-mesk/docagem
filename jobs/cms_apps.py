# -*- coding: utf-8 *-*
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


@apphook_pool.register
class Resourceshook(CMSApp):
    name = _("Jobs")

    def get_urls(self, page=None, language=None, **kwargs):
        # replace this with the path to your application's URLs module
        return ["jobs.urls"]

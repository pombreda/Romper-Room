from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.http import HttpResponse
from dj4sq.views import OAuthReceiver
from main.views import HomeView, ExploreView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(template_name='index.html'), name='home'),

    url(r'^explore$', login_required(ExploreView.as_view())),
    url(r'^oauth/foursquare$', OAuthReceiver.as_view()),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^robots.txt$', lambda x: HttpResponse("User-Agent: *\nDisallow: /",
                                                mimetype="text/plain")),
)

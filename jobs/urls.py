from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /chapter/
    url('^$', views.chapter_list, name='chapter_list'),
    # ex: /tudo/
    url('^tudo/$', views.chapter_all, name='chapter_all'),
    # ex: /chapter/5/1/1
    url('^(?P<chapter_id>[0-9]+)/(?P<item_number>[0-9]+)/(?P<subitem_number>[0-9]+)/$', views.subitem_detail, name='subitem_detail'),
    # ex: /chapter/5/1
    url('^(?P<chapter_id>[0-9]+)/(?P<item_number>[0-9]+)/$', views.item_detail, name='item_detail'),
    # ex: /chapter/5/
    url('^(?P<chapter_id>[0-9]+)/$', views.chapter_detail, name='chapter_detail'),
    # ex: /chapter/5/results/
    #url('<int:question_id>/results/', views.results, name='results'),
    # ex: /chapter/5/vote/
    #url('<int:question_id>/vote/', views.vote, name='vote'),
]
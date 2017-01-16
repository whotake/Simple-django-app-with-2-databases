from django.conf.urls import url
from . import views

app_name = 'store'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^item/(?P<item_id>[0-9]+)/$', views.item_page, name='detail'),
    url(r'^categorys/$', views.CatListView.as_view(), name='catList'),
    url(r'^category/(?P<category_id>[0-9]+)/$', views.category, name='category'),
    url(r'^(?P<item_id>[0-9]+)/add_comment/$', views.add_comment, name='add_comment'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^(?P<item_id>[0-9]+)/buy/$', views.create_order, name='create_order'),
    url(r'^search/$', views.search, name='search'),
    url(r'^orders/$', views.user_orders, name='user_orders'),
    url(r'^comments/$', views.user_comments, name='user_comments'),
    url(r'^(?P<comment_id>[0-9]+)/delete/$', views.delete_comment, name='delete_comment'),
    url(r'^(?P<comment_id>[0-9]+)/edit_page/$', views.edit_comment_page, name='edit_comment_page'),
    url(r'^(?P<comment_id>[0-9]+)/edit/$', views.edit_comment, name='edit_comment'),
]

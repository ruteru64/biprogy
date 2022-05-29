from xml.parsers.expat import model
from django.urls import path
from . import views
from . import models
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_account, name='create_account'),
    path('login/', views.account_login, name='login'),
    # pa    th('logout/', logout, {'template_name': 'index.html'}, name='logout'),
    path('logout/', LogoutView.as_view(template_name='index.html'), name="logout"),
    path('<int:user_id>/<int:partner_id>/topic',
         views.topic_deck, name='topic_deck'),
    path('<int:user_id>/<int:partner_id>/topic/post',
         views.post_topic, name='post_topic'),
    # path('<int:user_id>/partner', views.select_partner, name='select_partner')
    # path('', views.topic_post, name='add_partner')
    path('<int:user_id>/add_partner/', views.add_partner, name='add_partner'),
    path('<int:user_id>/<int:partner_id>/topic/api',
         views.topic_deck_api, name='topic_deck_api'),
    path('<int:user_id>/<int:partner_id>/topic/post/api',
         views.post_topic_api, name='post_topic_api'),
    path('<int:user_id>/<int:partner_id>/test', views.test, name='test')
]

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
    # path('logout/', logout, {'template_name': 'index.html'}, name='logout'),
    path('logout/', LogoutView.as_view(template_name='index.html'), name="logout"),
    path('<int:user_id>/<int:partner_id>/topic',
         views.topic_deck, name='topic_deck')
    # path('', views.topic_post, name='topic_post')
    # path('<int:user_id>/partner', views.select_partner, name='select_partner')
    # path('', views.topic_post, name='add_partner')
    # path()
]

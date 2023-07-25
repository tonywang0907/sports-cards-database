from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('index/', views.index, name="index"),
    path('market/', views.market, name="market"),
    path('add_card/', views.add_card, name="add_card"),
    path('store_card/', views.store_card, name="store_card"),
    path('delete/<int:card_id>/', views.delete_card, name="delete_card"),
    path('edit_card/<int:card_id>', views.edit_card, name="edit_card"),
    path('card_info/<int:card_id>', views.card_info, name="card_info"),
    path('toggle_tag/<int:card_id>/<str:tag_name>/', views.toggle_tag, name='toggle_tag'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

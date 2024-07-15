from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('login-l/', views.user_login_l, name='login-l'),
    path('register/', views.register, name='register'),
    path('register-l/', views.register_l, name='register-l'),
    path('', views.ListOfDishes, name='dishes'),
    path('light/', views.ListOfDishesLight, name='dishes-l'),
    path('more/<int:pk>/', views.DetailDish, name='more'),
    path('more-l/<int:pk>/', views.DetailDish_l, name='more-l'),
    path('logout', views.logout_view, name='logout'),
    path('logout-l', views.logout_view_l, name='logout-l'),
    path('soda/', views.ListOfDishesSoda, name='soda'),
    path('alco/', views.ListOfDishesAlco, name='alco'),
    path('desert/', views.ListOfDishesDesert, name='desert'),
    path('first/', views.ListOfDishesFirst, name='first'),
    path('sec/', views.ListOfDishesSec, name='sec'),
    path('fast/', views.ListOfDishesFast, name='fast'),
    path('salat/', views.ListOfDishesSalat, name='salat'),
    path('tuck/', views.ListOfDishesTuck, name='tuck'),
    path('soda-l/', views.ListOfDishesSoda_l, name='soda-l'),
    path('alco-l/', views.ListOfDishesAlco_l, name='alco-l'),
    path('desert-l/', views.ListOfDishesDesert_l, name='desert-l'),
    path('first-l/', views.ListOfDishesFirst_l, name='first-l'),
    path('sec-l/', views.ListOfDishesSec_l, name='sec-l'),
    path('fast-l/', views.ListOfDishesFast_l, name='fast-l'),
    path('salat-l/', views.ListOfDishesSalat_l, name='salat-l'),
    path('tuck-l/', views.ListOfDishesTuck_l, name='tuck-l'),
    path('corsina/', views.connect_to_corsina, name='corsina'),
    path('corsina-l/', views.connect_to_corsina_l, name='corsina-l'),
    path('more/<int:pk>/pay/', views.pay, name='payment'),
    path('more-l/<int:pk>/pay-l/', views.pay_l, name='payment-l'),
    path('pay/success/', views.success, name='success'),
    path('pay-l/success-l/', views.success_l, name='success-l'),
    path('about_us/', views.about_us, name='about us'),
    path('about_us_l/', views.about_us_l, name='about us-l'),
    path('more/<int:pk>/quan', views.quan, name='quan'),
    path('more-l/<int:pk>/quan', views.quan_l, name='quan-l'),
    path('more/<int:pk>/is18/', views.iseighteen, name='is18'),
    path('more-l/<int:pk>/is18-l/', views.iseighteen_l, name='is18-l'),
    path('saled/', views.connect_to_saled, name='saled'),
    path('saled-l/', views.connect_to_saled_l, name='saled-l'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

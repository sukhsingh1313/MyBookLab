from django.urls import path
from . import views
from accounts.views import signup_view,otp_verification,login_view,logout_view

from django.contrib.auth.views import (  PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,)


urlpatterns = [
    path('view/<slug:slug>/<str:format_type>/',views.open_book_function,name='view_book'),
     path('purchase/<int:book_id>/', views.purchase_book, name='purchase_book'),
    path('',views.main_book_section,name='main_book_section'),
    path('book/<slug:slug>/',views.BookDetail_view,name='BookDetail_view'),
    path('search/', views.search_books_view, name='search'),
    path('books/',views.all_books_view, name='book_list'),
    path('contect/',views.contect_view, name='contect_view'),


    #account section urls
    path('register/',signup_view, name='signup_view'),
    path('otp-verification/<int:user_id>/', otp_verification, name='otp_verification'),
    path('login/',login_view, name='login_view'),
    path('logout/',logout_view, name='logout_view'),

    
    # password session
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]

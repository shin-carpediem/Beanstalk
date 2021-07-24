from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'restaurant'
urlpatterns = [
    path('login/', views.login_as_user, name='login'),
    # path('confirm/', views.confirm, name='confirm'),
    path('order_manage/', views.order_manage, name='order_manage'),
    path('order_manage/change/', views.order_status_ch, name='order_status_ch'),
    path('order_manage/history/', views.history, name='history'),
    path('order_manage/history/total/', views.total, name='total'),
    path('order_manage/history/total/stop/', views.stop_user_order, name='stop_user_order'),
    path('order_manage/history/daily/', views.daily, name='daily'),
    path('manage/login/', views.manage_login, name='manage_login'),
    path('manage/company/logo', views.company_logo, name='company_logo'),
    path('manage/company/name', views.company_name, name='company_name'),
    path('manage/menu/', views.manage_menu, name='manage_menu'),
    path('manage/menu/add', views.category_add, name='category_add'),
    path('manage/menu/change', views.category_ch, name='category_ch'),
    path('manage/menu/delete', views.category_del, name='category_del'),
    path('manage/menu/category/change', views.category_menu_ch, name='category_menu_ch'),
    path('manage/menu/menu/add', views.menu_add, name='menu_add'),
    path('manage/menu/menu/delete', views.menu_del, name='menu_del'),
    path('manage/menu/img', views.menu_img_manage, name='menu_img_manage'),
    path('manage/menu/name', views.menu_name_manage, name='menu_name_manage'),
    path('manage/menu/price', views.menu_price_manage, name='menu_price_manage'),
    path('manage/menu/allergy/change', views.allergy_ch, name='allergy_ch'),
    path('manage/menu/allergy/item/add', views.allergy_add, name='allergy_add'),
    path('manage/menu/allergy/item/delete',
         views.allergy_del, name='allergy_del'),
    path('manage/menu/nomiho/add', views.nomiho_add, name='nomiho_add'),
    path('manage/menu/nomiho/change', views.nomiho_ch, name='nomiho_ch'),
    path('manage/menu/nomiho/delete', views.nomiho_del, name='nomiho_del'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

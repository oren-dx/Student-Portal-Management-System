from django.urls import path
from portal_app.views import*

urlpatterns = [
    path('', login_view, name='login_view'),
    path('register/', register_view, name='register_view'),
    path('logout/', logout_view, name='logout_view'),
    
    path('dashboard/',dashboard, name='dashboard'),
    path('student-list/',student_list, name='student_list'),
    
    
    path('student/add/', student_create, name='student_create'),
    path('student/<int:s_id>/', student_detail, name='student_detail'),
    path('student/update/<int:s_id>/', student_update, name='student_update'),
    path('student/delete/<int:s_id>/', student_delete, name='student_delete'),
    
    path('results/', result_list, name='result_list'),
    path('results/add/', result_create, name='result_create'),
    path('results/update/<int:r_id>/',result_update,name='result_update'),
    path('results/delete/<int:r_id>/',result_delete, name='result_delete'),

    
    path('fee/list/', fee_list, name='fee_list'),
    path('fee/create/', fee_create, name='fee_create'),
    path('fees/update/<int:f_id>/',fee_update, name='fee_update'),


    path('payment/list', payment_list, name='payment_list'),
    path('payment/create/', payment_create, name='payment_create'),
    
]

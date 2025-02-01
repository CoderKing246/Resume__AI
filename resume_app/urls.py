from django.urls import path
from . import views



urlpatterns = [
    path('',views.home),
    path('upload-resume',views.upload_resume,name='upload'),
    path('delete/<int:id_resume>',views.delete,name='delete_resume'),
    path('about/',views.about),
    path('contact/',views.contact),
    path('login/',views.login_page,name='login'),
    path('register/',views.register_page,name='register'),
    path('logout/',views.logout_page,name="logout"),
    path('resume-list/',views.resume_list,name="resume_list")
    
    
    
]

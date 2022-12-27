from django.urls import path
from . import views

urlpatterns = [
    path('',views.Utils.login,name='login'),
    path('enseignant/',views.Enseignant.teachers,name='teachers'),
    path('surveillant/',views.Surveillant.controllers,name='controllers'),
    path('surveillant/inscrire/',views.Surveillant.inscrire,name='inscrire'),
    path('surveillant/vote/',views.Surveillant.voirVote,name='voirVote'),
    path('surveillant/enseignant/',views.Surveillant.inscrireDeja,name='inscrireDeja'),
    path('surveillant/password/',views.Surveillant.passwordReset,name='passwordReset'),
    path('surveillant/page/',views.Surveillant.printable,name='printable'),
    path('surveillant/<int:pk>/password/',views.Surveillant.validePasswordDetail,name='validePasswordDetail'),
    path('surveillant/suggestions/',views.Surveillant.suggestions,name='suggestions'),
    path('logout/',views.Utils.logoutUser,name='logoutUser'),
    path('login/',views.Utils.login,name='login'),
    path('surveillant/deleteUser/',views.Ajax.delete,name='deleteUser'),
    path('surveillant/validePassword/',views.Ajax.validePassword,name='validePassword'),
    path('checkClass/',views.Ajax.listClassFetch,name='checkClass'),
    path('ifExist/',views.Ajax.classExist,name='ifExist'),
    path('askPasswd/',views.Ajax.askNewPasswd,name='askNewPasswd'),
    path('reviewSave/',views.Ajax.reviewSave,name="reviewSave"),
    path('unNew/',views.Ajax.unNew,name='unNew'),
    path('api/test/', views.Ajax.vuejs, name="vuejs"),

]

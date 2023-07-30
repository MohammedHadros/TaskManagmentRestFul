from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import apply_suffix_patterns

router = DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
    path("tasks" , All_Task , name="all-tasks"),
    path("tasks/<int:pk>" , task_detiles , name="task-view"),
    path("tasks/<int:pk>/file" , All_Task_Files , name="task-file"),
    path("comments" , All_Comments , name="comments"),
    path("comments/task/<int:pk>" , Add_Comments , name="comments"),
    path("change_request/" , All_Change_request , name="requests"),
    path("change_request/task/<int:pk>" , New_Rwquest , name="change-employee"),
    path("change_request/task/<int:pk>/req/<int:req_pk>" , Response_Form , name="change-employee"),
    # path("upload/file/task/<int:pk>" , UploadFile , name="upload-file"),

]

# urlpatterns=apply_suffix_patterns(urlpatterns)
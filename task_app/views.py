from django.shortcuts import render
from django.http import JsonResponse
from .models import Task,Task_Files,Comment,Chaange_request
from .serializers import (TaskSerializer,TaskFilesSerializer,TaskSerializerUpdate
                          ,CommentSerializer,RequestChangeSerializer ,RequestResponseSerializer )
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

@api_view(['GET' , "POST"])
def All_Task(request ):
    if request.method=='GET':
        tasks=Task.objects.all()
        task_serializer = TaskSerializer(tasks,many=True)
        return Response(  task_serializer.data )
    #Add new task =>>
    elif request.method=='POST':
        task_serializer=TaskSerializer(data=request.data )
        if task_serializer.is_valid():
            task_serializer.save()
            return Response(task_serializer.data , status=status.HTTP_201_CREATED)


#CURD operation on each task
@api_view(['GET' , "PUT" , "DELETE"])
def task_detiles(request , pk ):
    try:
        task=Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response( status=status.HTTP_404_NOT_FOUND)

    if request.method=='GET':
        serializer = TaskSerializer(task)
        comments=Comment.objects.filter(task=task)
        task_file=Task_Files.objects.filter(task=task)
        com_serializer=CommentSerializer(comments,many=True)
        file_serializer=TaskFilesSerializer(task_file,many=True)
        return Response({"Task" : serializer.data, "Comments":com_serializer.data , "files":file_serializer.data} )
    elif request.method=='PUT':
        serializer=TaskSerializerUpdate(task,data=request.data )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


#File managment
@api_view(['GET' , "POST"])
def All_Task_Files(request ,pk):
    if request.method=='GET':
        task=Task.objects.get(pk=pk)
        task_files=Task_Files.objects.filter(task=task)
        serializer = TaskFilesSerializer(task_files,many=True)
        return Response(  serializer.data )
    elif request.method=='POST':
        task_serializer=TaskFilesSerializer(data=request.data )
        if task_serializer.is_valid():
            task_serializer.save()
            return Response(task_serializer.data , status=status.HTTP_201_CREATED)

@api_view(['GET' ])
def All_Comments(request ):
    if request.method=='GET':
        Comments=Comment.objects.all()
        serializer = CommentSerializer(Comments,many=True)
        return Response(  serializer.data )

@api_view(['GET' , "POST"])
def Add_Comments(request,pk ):
    task=Task.objects.get(pk=pk)
    if request.method=='GET':
        Comments=Comment.objects.filter(task=task)
        serializer = CommentSerializer(Comments,many=True)
        return Response(  serializer.data )
    elif request.method=='POST':
        data=request.data
        data["task"]=task.id
        data["user"]=request.user.id
        serializer=CommentSerializer(data=data )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)


@api_view(['GET'])
def All_Change_request(request ):
    if request.method=='GET':
        change_user=Chaange_request.objects.all()
        serializer = RequestChangeSerializer(change_user,many=True)
        return Response(  serializer.data )

@api_view(["GET","POST"])
def New_Rwquest(request,pk):
    task = Task.objects.get(pk=pk)
    if request.method=='GET':
        change_user=Chaange_request.objects.filter(task=task)
        serializer = RequestChangeSerializer(change_user,many=True)
        return Response(  serializer.data )
    elif request.method=='POST':
        request.data["task"]=task.pk
        if request.user.is_superuser:
            mydata=request.data
            mydata["creator"]=request.user.id
            task_serializer=RequestChangeSerializer(data=mydata )
            if task_serializer.is_valid():
                task_serializer.save()
                return Response(task_serializer.data , status=status.HTTP_201_CREATED)
        else:
            return Response( status=status.HTTP_401_UNAUTHORIZED)


@api_view(["GET", "PUT"])
def Response_Form(request,pk , req_pk):
    task = Task.objects.get(pk=pk)
    req_change=Chaange_request.objects.get(pk=req_pk)
    if request.method=='GET':
        if req_change.new_user.id==request.user.id:
            serializer = RequestChangeSerializer(req_change)
            return Response(  serializer.data )
    elif request.method=='PUT':
        if req_change.task==task:
            print(req_change.new_user)
            print(request.user)
            if req_change.new_user.id==request.user.id:
                task_serializer=RequestResponseSerializer(req_change,data=request.data )
                if task_serializer.is_valid():
                    task_serializer.save()
                    subject="Response from Employee"
                    sender_email=settings.EMAIL_HOST_USER
                    to=request.user.email
                    if request.data["status"]==1:
                        massage="Request has been approved"
                    elif request.data["status"]==2:
                        massage="Request has been rejected"
                    else:
                        massage="No response yet "

                    send_mail(subject,
                              massage,
                              sender_email,
                              [to]
                              )

                    return Response(task_serializer.data , status=status.HTTP_201_CREATED)
        return Response( status=status.HTTP_401_UNAUTHORIZED)


# def UploadFile(request , pk):
#     task=Task.objects.get(pk=pk)
#     if request.method=='POST':
#         task_serializer=TaskFilesSerializer(data=request.data )
#         if task_serializer.is_valid():
#             task_serializer.save()
#             return Response(task_serializer.data , status=status.HTTP_201_CREATED)
#     return render (request , "upload_file.html")



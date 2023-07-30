# countries/serializers.py
from rest_framework import serializers
from task_app.models import Comment ,Task ,Task_Files,Chaange_request



# convert model into json and what data to include
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "assigned_to","difficulty"]#,"created_at","updated_at"

class TaskSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "difficulty","updated_at"]#,"created_at","updated_at"

class TaskFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task_Files
        fields = ["id", "task", "file"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "comment", "user" ,"task"]#,"created_at"

class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "comment" ,"task"]#,"created_at"

class RequestChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chaange_request
        fields = ["id", "task" , "old_user","new_user","creator" ,"status" ]#,"created_at"

class RequestResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chaange_request
        fields = ["status" ]#,"created_at"
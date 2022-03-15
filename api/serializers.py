from rest_framework.serializers import ModelSerializer
from api.models import Todos
from django.contrib.auth.models import User
class TodoSerializer(ModelSerializer):
    class Meta:
        model=Todos
        fields=['id','task_name','completed_status','user']
        read_only_fields=['id','user']
        depth=1
class UsercreationSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['username','password','email']
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
from rest_framework import serializers
from todowooApp.models import todowooApp

class TodoSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    datecompleted = serializers.ReadOnlyField()


    class Meta:
        model = todowooApp
        fields = ['id','title','memo','created','datecompleted','important']


class TodoCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = todowooApp
        fields = ['id']
        read_only_fields = ['id','title','memo','created','datecompleted','important']


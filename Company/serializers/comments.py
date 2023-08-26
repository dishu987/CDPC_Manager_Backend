from rest_framework import serializers
from Company.models import Comment
from django.utils.timesince import timesince
from users.models import UserModel

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id','name',)


class CommentAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('company', 'text','reply_to')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        comment = Comment.objects.create(**validated_data)
        return comment

class ReplySerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        formatted_time = obj.created_at.strftime("%A, %B %Y %I:%M%p")
        time_ago = timesince(obj.created_at)
        return f"{formatted_time} ({time_ago} ago)"

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'created_at')

class CommentSerializer(serializers.ModelSerializer):
    user = UserModelSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        formatted_time = obj.created_at.strftime("%A, %B %Y %I:%M%p")
        time_ago = timesince(obj.created_at)
        return f"{formatted_time} ({time_ago} ago)"

    def get_replies(self, obj):
        # Retrieve only the direct replies for the comment
        replies = Comment.objects.filter(reply_to=obj, reply_to__isnull=False).exclude(id=obj.id)
        serializer = CommentSerializer(replies, many=True)
        return serializer.data

    class Meta:
        model = Comment
        fields = ('id', 'company', 'user', 'text', 'reply_to', 'created_at', 'replies')

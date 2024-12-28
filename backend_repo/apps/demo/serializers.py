from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')  # Get the author's username
    class Meta:
        model = Comment
        fields = ['id', 'text', 'timestamp', 'user']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)  # To display comments for each post
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)  # Comment count for post
    user = serializers.CharField(source='user.username')  # Get the author's username
    
    class Meta:
        model = Post
        fields = ['id', 'text', 'timestamp', 'user', 'comment_count', 'comments']

    def get_comments(self, obj):
        # Fetch the latest 3 Comments for each post 

        latest_comments = obj.comments.order_by('-timestamp')[:3]
        return CommentSerializer(latest_comments, many=True).data
        # Fetch 3 random comments for each post.
        # Instead of sorting comments by timestamp, we use Django's `order_by('?')` 
        # to retrieve a random order of comments and limit the result to 3.
        
        # This approach uses the `order_by('?')` query which returns a random ordering of rows
        # in the database, and we slice the result to get only 3 comments.
        # Uncomment the below code for random comments
        # random_comments = obj.comments.order_by('?')[:3]
        # return CommentSerializer(random_comments, many=True).data
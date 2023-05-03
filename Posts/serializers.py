from rest_framework import serializers, status


from .models import Post

class PostSerializer(serializers.ModelSerializer):


    def validate_status(self, value):

        if value not in [1, 2]:
            raise serializers.ValidationError("Status must be 1 or 2.")
        return value


    class Meta:
        model = Post
        fields = ('id', 'title', 'sub_title', 'text', 'image', 'status', 'dateOfPublish', 'author')
        read_only_fields = ('id', 'dateOfPublish', 'author')






# class PostSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=80, required=True)
#     sub_title = serializers.CharField(max_length=80, required=True)
#     text = serializers.CharField(required=True)
#     image = serializers.ImageField(required=False)
#     status = serializers.IntegerField(required=True)
#     author_id = serializers.IntegerField(required=True)

from rest_framework import serializers, status


from .models import Post,ImagePost

class PostSerializer(serializers.ModelSerializer):


    def validate_status(self, value):

        if value not in [1, 2]:
            raise serializers.ValidationError("Status must be 1 or 2.")
        return value


    class Meta:
        model = Post
        fields = ('id', 'title', 'sub_title', 'text', 'image', 'status', 'dateOfPublish', 'author')
        read_only_fields = ('id', 'dateOfPublish', 'author')



class ImagesSerializer(serializers.ModelSerializer):
    # text = serializers.CharField()

    class Meta:
        model = ImagePost
        fields = '__all__'


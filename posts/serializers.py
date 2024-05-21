from rest_framework import serializers
from .models import Post
from likes.models import Like


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()

    @staticmethod
    def validate_banner(value):
        if value.size > 1024 * 1024:
            raise serializers.ValidationError('Banner size is larger than 1MB')
        if value.height > 2560:
            raise serializers.ValidationError('Banner height is larger than 2560px')
        if value.width > 1440:
            raise serializers.ValidationError('Banner height is larger than 1440px')
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner=user, post=obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = Post
        fields = [
            'id', 'owner', 'is_owner', 'profile_id', 'profile_image', 'created_at', 'updated_at', 'is_published',
            'title', 'sub_title', 'slug', 'banner', 'body', 'gmap_location_tag', 'like_id',  'likes_count',
            'comments_count',
        ]

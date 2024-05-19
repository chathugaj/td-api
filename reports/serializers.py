from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    """
    Serializer for the Report model
    """
    reporter = serializers.ReadOnlyField(source='reporter.username')
    is_reporter = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='reporter.profile.id')
    profile_image = serializers.ReadOnlyField(source='reporter.profile.image.url')

    def get_is_reporter(self, obj):
        request = self.context['request']
        return request.user == obj.reporter

    class Meta:
        model = Report
        fields = [
            'id', 'reporter', 'is_reporter', 'profile_id', 'profile_image', 'reason', 'message', 'created_at', 'updated_at'
        ]
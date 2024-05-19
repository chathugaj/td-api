from rest_framework import generics, permissions

from reports.models import Report
from reports.serializers import ReportSerializer
from td_api.permissions import IsOwner


class ReportList(generics.ListCreateAPIView):
    """
        Facilitates the list and report API endpoints
        """
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAdminUser, IsOwner]
    queryset = Report.objects.all()

    def perform_create(self, serializer):
        """Creates a report"""
        serializer.save(reporter=self.request.user)


class ReportDetail(generics.RetrieveUpdateAPIView):
    """Facilitates get, update a specific report"""
    permission_classes = [IsOwner]
    serializer_class = ReportSerializer
    queryset = Report.objects.all()

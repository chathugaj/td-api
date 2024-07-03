from rest_framework import generics, permissions

from reports.models import Report
from reports.serializers import ReportSerializer
from td_api.pagination import StandardResultsSetPagination
from td_api.permissions import IsOwner


class ReportList(generics.ListCreateAPIView):
    """
    Facilitates the list and report API endpoints
    """
    serializer_class = ReportSerializer
    permission_classes = [IsOwner|permissions.IsAdminUser]
    pagination_class = StandardResultsSetPagination
    queryset = Report.objects.all()

    def perform_create(self, serializer):
        """Creates a report"""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Report.objects.all()
        else:
            return Report.objects.all().filter(owner=self.request.user.id)


class ReportDetail(generics.RetrieveUpdateAPIView):
    """Facilitates get, update a specific report"""
    permission_classes = [permissions.IsAuthenticated|permissions.IsAdminUser]
    serializer_class = ReportSerializer
    http_method_names = ['get', 'put']
    queryset = Report.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Report.objects.all()
        else:
            return Report.objects.all().filter(owner=self.request.user.id)

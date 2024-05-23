from django.urls import path

from reports.views import ReportList, ReportDetail

urlpatterns = [
    path('contacts/', ReportList.as_view()),
    path('contacts/<int:pk>/', ReportDetail.as_view())
]
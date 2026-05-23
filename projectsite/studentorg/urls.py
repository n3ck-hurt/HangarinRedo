from django.urls import path

from .views import (
    CollegeListView,
    HomePageView,
    OrganizationCreateView,
    OrganizationDeleteView,
    OrganizationList,
    OrganizationUpdateView,
    OrgMemberListView,
    ProgramListView,
    StudentListView,
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('organization_list', OrganizationList.as_view(), name='organization-list'),
    path('organization_list/add', OrganizationCreateView.as_view(), name='organization-add'),
    path('organization_list/<pk>', OrganizationUpdateView.as_view(), name='organization-update'),
    path('organization_list/<pk>/delete', OrganizationDeleteView.as_view(), name='organization-delete'),
    path('members/', OrgMemberListView.as_view(), name='orgmember-list'),
    path('students/', StudentListView.as_view(), name='student-list'),
    path('colleges/', CollegeListView.as_view(), name='college-list'),
    path('programs/', ProgramListView.as_view(), name='program-list'),
]

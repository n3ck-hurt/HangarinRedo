from django.urls import path

from .views import (
    CollegeCreateView,
    CollegeDeleteView,
    CollegeListView,
    CollegeUpdateView,
    HomePageView,
    OrganizationCreateView,
    OrganizationDeleteView,
    OrganizationList,
    OrganizationUpdateView,
    OrgMemberCreateView,
    OrgMemberDeleteView,
    OrgMemberListView,
    OrgMemberUpdateView,
    ProgramCreateView,
    ProgramDeleteView,
    ProgramListView,
    ProgramUpdateView,
    StudentCreateView,
    StudentDeleteView,
    StudentListView,
    StudentUpdateView,
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    # Firearms
    path('firearms/', OrganizationList.as_view(), name='organization-list'),
    path('firearms/add/', OrganizationCreateView.as_view(), name='organization-add'),
    path('firearms/<pk>/', OrganizationUpdateView.as_view(), name='organization-update'),
    path('firearms/<pk>/delete/', OrganizationDeleteView.as_view(), name='organization-delete'),
    # Sales
    path('sales/', OrgMemberListView.as_view(), name='orgmember-list'),
    path('sales/add/', OrgMemberCreateView.as_view(), name='orgmember-add'),
    path('sales/<pk>/', OrgMemberUpdateView.as_view(), name='orgmember-update'),
    path('sales/<pk>/delete/', OrgMemberDeleteView.as_view(), name='orgmember-delete'),
    # Customers
    path('customers/', StudentListView.as_view(), name='student-list'),
    path('customers/add/', StudentCreateView.as_view(), name='student-add'),
    path('customers/<pk>/', StudentUpdateView.as_view(), name='student-update'),
    path('customers/<pk>/delete/', StudentDeleteView.as_view(), name='student-delete'),
    # Categories
    path('categories/', CollegeListView.as_view(), name='college-list'),
    path('categories/add/', CollegeCreateView.as_view(), name='college-add'),
    path('categories/<pk>/', CollegeUpdateView.as_view(), name='college-update'),
    path('categories/<pk>/delete/', CollegeDeleteView.as_view(), name='college-delete'),
    # Calibers
    path('calibers/', ProgramListView.as_view(), name='program-list'),
    path('calibers/add/', ProgramCreateView.as_view(), name='program-add'),
    path('calibers/<pk>/', ProgramUpdateView.as_view(), name='program-update'),
    path('calibers/<pk>/delete/', ProgramDeleteView.as_view(), name='program-delete'),
]

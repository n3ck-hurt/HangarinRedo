from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from studentorg.forms import OrganizationForm
from studentorg.mixins import SearchableListMixin, SortableListMixin
from studentorg.models import College, OrgMember, Organization, Program, Student


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = timezone.now().year
        context.update({
            'organizations_count': Organization.objects.count(),
            'students_count': Student.objects.count(),
            'programs_count': Program.objects.count(),
            'colleges_count': College.objects.count(),
            'org_members_count': OrgMember.objects.count(),
            'students_joined_this_year': (
                OrgMember.objects.filter(date_joined__year=year)
                .values('student')
                .distinct()
                .count()
            ),
        })
        return context


class OrganizationList(LoginRequiredMixin, SearchableListMixin, ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'org_list.html'
    paginate_by = 5
    search_fields = ('name', 'description', 'college__college_name')

    def get_queryset(self):
        return super().get_queryset().select_related('college')


class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_form.html'
    success_url = reverse_lazy('organization-list')


class OrganizationUpdateView(LoginRequiredMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_form.html'
    success_url = reverse_lazy('organization-list')


class OrganizationDeleteView(LoginRequiredMixin, DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')


class OrgMemberListView(LoginRequiredMixin, SearchableListMixin, SortableListMixin, ListView):
    model = OrgMember
    context_object_name = 'members'
    template_name = 'orgmember_list.html'
    paginate_by = 10
    search_fields = (
        'student__lastname',
        'student__firstname',
        'organization__name',
    )
    sort_fields = ('student__lastname', 'date_joined', 'organization__name')
    default_sort = 'student__lastname'

    def get_queryset(self):
        return super().get_queryset().select_related('student', 'organization')


class StudentListView(LoginRequiredMixin, SearchableListMixin, ListView):
    model = Student
    context_object_name = 'students'
    template_name = 'student_list.html'
    paginate_by = 10
    search_fields = (
        'student_id',
        'lastname',
        'firstname',
        'program__prog_name',
    )

    def get_queryset(self):
        return super().get_queryset().select_related('program')


class CollegeListView(LoginRequiredMixin, SearchableListMixin, ListView):
    model = College
    context_object_name = 'colleges'
    template_name = 'college_list.html'
    paginate_by = 5
    search_fields = ('college_name',)


class ProgramListView(LoginRequiredMixin, SearchableListMixin, SortableListMixin, ListView):
    model = Program
    context_object_name = 'programs'
    template_name = 'program_list.html'
    paginate_by = 10
    search_fields = ('prog_name', 'college__college_name')
    sort_fields = ('prog_name', 'college__college_name')
    default_sort = 'prog_name'

    def get_queryset(self):
        return super().get_queryset().select_related('college')

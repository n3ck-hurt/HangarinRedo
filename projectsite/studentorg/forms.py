from django.forms import ModelForm, DateInput
from .models import Organization, Student, College, Program, OrgMember


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


class CollegeForm(ModelForm):
    class Meta:
        model = College
        fields = '__all__'


class ProgramForm(ModelForm):
    class Meta:
        model = Program
        fields = '__all__'


class OrgMemberForm(ModelForm):
    class Meta:
        model = OrgMember
        fields = '__all__'
        widgets = {
            'date_joined': DateInput(attrs={'type': 'date'}),
        }

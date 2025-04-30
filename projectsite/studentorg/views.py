import json
from django.shortcuts import render

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import Organization, OrgMember, Student, College, Program
from studentorg.forms import OrganizationForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.db.models import Count, F, Q
from datetime import datetime

@method_decorator(login_required, name='dispatch')
# Home Page View
class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = 'home.html'

from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q

# Organization Views
class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'org_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(OrganizationList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(name__icontains=query) |
                           Q(college__college_name__icontains=query) |
                           Q(description__icontains=query))
        return qs

class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_add.html'
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_edit.html'
    success_url = reverse_lazy('organization-list')

class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')

# OrgMember Views
class OrgMemberList(ListView):
    model = OrgMember
    context_object_name = 'orgmember'
    template_name = 'orgmember_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(OrgMemberList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(student__firstname__icontains=query) |
                           Q(student__lastname__icontains=query) |
                           Q(organization__name__icontains=query) |
                           Q(date_joined__icontains=query))
        return qs

class OrgMemberCreateView(CreateView):
    model = OrgMember
    fields = '__all__'
    template_name = 'orgmember_add.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    fields = '__all__'
    template_name = 'orgmember_edit.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    template_name = 'orgmember_del.html'
    success_url = reverse_lazy('orgmember-list')

# Student Views
class StudentList(ListView):
    model = Student
    context_object_name = 'student'
    template_name = 'student_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(StudentList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(firstname__icontains=query) |
                           Q(lastname__icontains=query) |
                           Q(student_id__icontains=query) |
                           Q(program__prog_name__icontains=query))
        return qs

class StudentCreateView(CreateView):
    model = Student
    fields = '__all__'
    template_name = 'student_add.html'
    success_url = reverse_lazy('student-list')

class StudentUpdateView(UpdateView):
    model = Student
    fields = '__all__'
    template_name = 'student_edit.html'
    success_url = reverse_lazy('student-list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_del.html'
    success_url = reverse_lazy('student-list')

# College Views
class CollegeList(ListView):
    model = College
    context_object_name = 'college'
    template_name = 'college_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(CollegeList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(college_name__icontains=query))
        return qs

class CollegeCreateView(CreateView):
    model = College
    fields = '__all__'
    template_name = 'college_add.html'
    success_url = reverse_lazy('college-list')

class CollegeUpdateView(UpdateView):
    model = College
    fields = '__all__'
    template_name = 'college_edit.html'
    success_url = reverse_lazy('college-list')

class CollegeDeleteView(DeleteView):
    model = College
    template_name = 'college_del.html'
    success_url = reverse_lazy('college-list')

# Program Views
class ProgramList(ListView):
    model = Program
    context_object_name = 'program'
    template_name = 'program_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(ProgramList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(prog_name__icontains=query) |
                           Q(college__college_name__icontains=query))
        return qs

class ProgramCreateView(CreateView):
    model = Program
    fields = '__all__'
    template_name = 'program_add.html'
    success_url = reverse_lazy('program-list')

class ProgramUpdateView(UpdateView):
    model = Program
    fields = '__all__'
    template_name = 'program_edit.html'
    success_url = reverse_lazy('program-list')

class ProgramDeleteView(DeleteView):
    model = Program
    template_name = 'program_del.html'
    success_url = reverse_lazy('program-list')


# Dashboard View (Charts)
def dashboard(request):
    # Chart 1: Polar Area Chart - Distribution of students across programs
    program_distribution = {
        'labels': list(Program.objects.values_list('prog_name', flat=True)),
        'data': list(Program.objects.annotate(student_count=Count('student')).values_list('student_count', flat=True))
    }

    # Chart 2: Doughnut Chart - Percentage of students in each college
    college_distribution = {
        'labels': list(College.objects.values_list('college_name', flat=True)),
        'data': list(College.objects.annotate(student_count=Count('program__student')).values_list('student_count', flat=True))
    }

    # Chart 3: Horizontal Bar Chart - Top 5 organizations with the most members
    top_organizations = {
        'labels': list(Organization.objects.annotate(member_count=Count('orgmember')).order_by('-member_count')[:5].values_list('name', flat=True)),
        'data': list(Organization.objects.annotate(member_count=Count('orgmember')).order_by('-member_count')[:5].values_list('member_count', flat=True))
    }


    # Chart 4: Heatmap - Monthly organization member registrations
    monthly_registrations = OrgMember.objects.extra(
        select={'month': "strftime('%%m', date_joined)"}
    ).values('month').annotate(count=Count('id')).order_by('month')

    # Map numeric months to month names
    month_map = {
        "01": "January", "02": "February", "03": "March", "04": "April",
        "05": "May", "06": "June", "07": "July", "08": "August",
        "09": "September", "10": "October", "11": "November", "12": "December"
    }
    heatmap_data = {
        'labels': [month_map[entry['month']] for entry in monthly_registrations],
        'data': [entry['count'] for entry in monthly_registrations]
    }


    # Chart 5: Stacked Bar Chart - Number of students in each college grouped by program
    college_program_data = Program.objects.values(
        'college__college_name', 'prog_name'
    ).annotate(student_count=Count('student'))

    stacked_bar_labels = list(college_program_data.values_list('college__college_name', flat=True).distinct())
    stacked_bar_datasets = {}
    for entry in college_program_data:
        program_name = entry['prog_name']
        if program_name not in stacked_bar_datasets:
            stacked_bar_datasets[program_name] = [0] * len(stacked_bar_labels)
        stacked_bar_datasets[program_name][stacked_bar_labels.index(entry['college__college_name'])] = entry['student_count']


    # Context for Rendering the Dashboard
    context = {
        'program_distribution': program_distribution,
        'college_distribution': college_distribution,
        'stacked_bar_labels': stacked_bar_labels,
        'stacked_bar_datasets': stacked_bar_datasets,
        'top_organizations': top_organizations,
        'heatmap_data': heatmap_data,
    }
    return render(request, 'dashboard.html', context)
from django.shortcuts import render, redirect

# Create your views here.
from projects.forms import ProjectForm
from projects.models import Project


def create_projects(request):
    form = ProjectForm()
    print(request, "===")
    data = request.POST
    print(data, " === data===")

    if request.method == "POST":
        form = ProjectForm(data=data)
        if form.is_valid():
            form.save()
            # form = ProjectForm()
            return redirect('view_all_projects')

        else:
            print(form.errors)
    return render(request, "projects/create_project.html", {"form": form})


def get_projects(request):
    data = request.POST
    if data:
        key = data.get('filter')
        projects={} if key is None else Project.objects.filter(title__contains=key)
    else:
        projects = Project.objects.all().order_by("-date_created")

    return render(request, "projects/project_list.html", {"projects": projects})


def filter_projects(request):
    data = request.POST
    key = data.get('filter')

    if key is not None:
        projects = Project.objects.filter(title__contains=key)
    else:
        projects = {}
    return render(request, "projects/filtered_projects.html", {'projects': projects})


def retrieve_projects(request, id):
    if Project.objects.filter(id=id).exists():
        project = Project.objects.get(id=id)
    else:
        project = {}
    return render(request, "projects/project_details.html", {'project': project})


def update_project(request, id):
    project = Project.objects.get(id=id)
    form = ProjectForm(instance=project)
    data = request.POST

    if request.method == "POST":
        form = ProjectForm(instance=project, data=data)
        if form.is_valid():
            form.save()
            return redirect('project_details', id)

        else:
            print(form.errors)
    return render(request, "projects/update_details.html", {'project': project, 'form': form})


def delete_project(request, id):
    if Project.objects.filter(id=id).exists():
        Project.objects.get(id=id).delete()
        return redirect('view_all_projects')

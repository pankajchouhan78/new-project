from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Employee

# Create your views here.


def index(request):
    if request.method == "POST":
        name = request.POST.get("name")
        department = request.POST.get("department")
        dob = request.POST.get("dob")
        gender = request.POST.get("gender")
        profile = request.FILES.get("file")
        # print(profile)
        Employee.objects.create(
            ename=name, department=department, dob=dob, gender=gender, profile=profile
        )
        return redirect("index")
    else:
        employees = Employee.objects.all()
        return render(request, "index.html", {"employees": employees})


def delete_employee(request, pk=None):
    if pk is not None:
        emp = Employee.objects.get(pk=pk)
        emp.delete()
        return redirect("index")
    else:
        return HttpResponse("Employee not found")


def update_employee(request, pk=None):
    if pk is not None:
        emp = Employee.objects.get(pk=pk)
        if request.method == "POST":
            profile = request.FILES.get("file")
            emp.ename = request.POST.get("name")
            emp.department = request.POST.get("department")
            emp.gender = request.POST.get("gender")
            emp.phone = request.POST.get("phone")

            if profile is not None and profile != "":
                emp.profile = profile

            emp.save()
            return redirect("index")

        else:
            return render(request, "update_employee.html", {"employee": emp})

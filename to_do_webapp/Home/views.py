from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Value, CharField
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import date, timedelta
from Home.models import Task, attached_documents
from authentication.models import Profile
import calendar
from django.db.models import ExpressionWrapper, F

# Create your views here.

@login_required(login_url='Login')
def dashboard(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    pending_tasks = Task.objects.filter(user=user_profile,complete=False).count()
    done_tasks = Task.objects.filter(user=user_profile,complete=True).count()
    total_tasks = pending_tasks+done_tasks
    try:
        precentage=int(done_tasks/total_tasks*100)
    except:
        precentage=0

    context = {'user_profile': user_profile, 'users': users,'pending_tasks':pending_tasks,'done_tasks':done_tasks,
               'total_tasks':total_tasks,'precentage':precentage}
    return render(request,'dashboard.html',context)

@login_required(login_url='Login')
def calendar_view(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    context = {'user_profile': user_profile, 'users': users}
    return render(request,'calendar_view.html',context)


#getting all tasks for calendar
@login_required(login_url='Login')
def all_tasks_calender_view(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    task_list = Task.objects.filter(user=user_profile)

    all_tasks_list = []
    for item in task_list:
        data_dic = {}

        data_dic['title'] = item.title
        data_dic['start'] = str(item.ending_date.replace().isoformat()).split('+')[0]
        data_dic['end'] = str(item.ending_date.replace().isoformat()).split('+')[0]

        all_tasks_list.append(data_dic)


    return JsonResponse({'meeting_list': all_tasks_list}, safe=False)

@login_required(login_url='Login')
def get_chart_data(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)



    todays_date = date.today()
    months_ago = 6
    six_months_ago = todays_date - timedelta(days=(months_ago * 365 / 12))


    done_task = (Task.objects.annotate(month=ExtractMonth("creation_date")).values("month").annotate(complete=Value(Task.objects.filter(user=user_profile,complete=True).count())).order_by("month"))
    pending_task = (Task.objects.annotate(month=ExtractMonth("creation_date")).values("month").annotate(incomplete=Value(Task.objects.filter(user=user_profile,complete=False).count())).order_by("month"))
    print('Value of done task',done_task)
    print('Value of pending task',pending_task)



    done_jobs={}
    pending_jobs={}

    for item in done_task :
        done_jobs[calendar.month_name[item['month']]]=int(item['complete'])
    for item in pending_task :
        pending_jobs[calendar.month_name[item['month']]]=int(item['incomplete'])
























    return JsonResponse({'done_jobs': done_jobs,'pending_jobs':pending_jobs}, safe=False)


@login_required(login_url='Login')
def Settings(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)










    context = {'user_profile': user_profile, 'users': users}
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if len(fname) != 0:
            users.first_name = fname
        if len(lname) != 0:
            users.last_name = lname
        if len(email) != 0:
            users.email = email
        if len(phone) != 0:
            user_profile.phone = phone

        if len(address) != 0:

            user_profile.address = address

        if len(request.FILES) != 0:
            my_file = request.FILES['upload']

            if my_file.content_type == 'image/jpg' or my_file.content_type == 'image/jpeg' or my_file.content_type == 'image/png':
                user_profile.picture = request.FILES['upload']

                users.save()
                user_profile.save()

                messages.success(request, 'Data updated successfully')
                return redirect('Settings')

            messages.success(request, 'Only JPG, PNG & JPEG image type is allowed')
            return redirect('Settings')
        users.save()
        user_profile.save()
        messages.success(request, 'Data updated successfully')
        return redirect('Settings')

    return render(request, 'settings.html', context)



@login_required(login_url='Login')
def setting_security(request):




    if request.method == 'POST':
        users = User.objects.get(email=request.user.email)


        new_password = request.POST.get('new_password')


        if len(new_password) != 0:
            users.set_password(new_password)
            users.save()



            messages.info(request, 'Password updated successfully,Please Login with New Set Password')
            return redirect('Login')



    else:

        return redirect('Settings')


@login_required(login_url='Login')
def create_task(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    if request.method == 'POST':
        task_title=request.POST.get('task_title')


        task_description=request.POST.get('task_description')

        set_priority=request.POST.get('set_priority')
        due_date=request.POST.get('due_date')




        obj=Task.objects.create(user=user_profile,title=task_title,description=task_description,
                                complete=False,
                                nature_of_task=set_priority,ending_date=due_date)

        if len(request.FILES) != 0:
            my_file = request.FILES.getlist('associated_doc')

            for item in my_file:
                image_id = attached_documents.objects.create(associated_doc=item)
                obj.associated_documents.add(image_id)
                image_id.save()
                obj.save()






        obj.save()
        print('Task Added successfully.')
        messages.success(request, 'Task Added successfully.')
        return redirect('task_list_view')

    context = {'user_profile': user_profile, 'users': users}
    return render(request,'tasks/create_task.html',context)



@login_required(login_url='Login')
def task_edit(request,id):
    users = User.objects.get(username=request.user)
    task_info=Task.objects.get(pk=id)

    user_profile = Profile.objects.get(owner=users)
    if request.method == 'POST':
        task_title=request.POST.get('task_title')


        task_description=request.POST.get('task_description')

        set_priority=request.POST.get('set_priority')
        due_date=request.POST.get('due_date')
        is_complete=request.POST.get('is_complete')

        if len(task_title) != 0:
            task_info.first_name = task_title

        if len(task_description) != 0:
            task_info.description = task_description

        if len(set_priority) != 0:
            task_info.set_priority = set_priority

        if len(due_date) != 0:
            task_info.due_date = due_date

        if is_complete =='Yes':
            task_info.complete= True
        elif is_complete =='No':
            task_info.complete = False




        if len(request.FILES) != 0:
            my_file = request.FILES.getlist('proof_doc')

            for item in my_file:
                image_id = attached_documents.objects.create(proof_of_completion=item)
                task_info.associated_documents.add(image_id)
                image_id.save()
                task_info.save()






        task_info.save()

        messages.success(request, 'Task updated successfully.')
        return redirect('task_list_view')

    context = {'user_profile': user_profile, 'users': users,'task_info':task_info}
    return render(request,'tasks/edit_task.html',context)


@login_required(login_url='Login')
def task_list_view(request):
    users = User.objects.get(username=request.user)

    user_profile = Profile.objects.get(owner=users)
    user_tasks = Task.objects.filter(user=user_profile)


    context = {'user_profile': user_profile, 'users': users,'user_tasks':user_tasks}
    return render(request,'tasks/tasks_list_view.html',context)



@login_required(login_url='Login')
def delete_tasks(request):
    if request.method == 'POST':

        ids = request.POST.getlist('id[]')




        for id in ids:
            print('line no 808',id)
            x = Task.objects.get(pk=id)
            x.delete()

        print('Task deleted by:', request.user.username)


        return JsonResponse(
            'Task removed', safe=False
        )


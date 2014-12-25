from django.shortcuts import render
from models import User, Group, Task, Post, Badge, ForgotPasswordRequest
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
# return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def is_logged_in(request):
    if not request.method == "POST":
        return False
    try:
        pk = request.POST.get("pk", '1');
        user = User.objects.get(pk=int(pk))
        key1 = request.POST.get("key1", '1')
        key2 = request.POST.get("key2", '1')
        
        if key1 ==  user.key1 and key2 == user.key2:
            return user
    except:
        return False  
    return False

@csrf_exempt
def test(request):
    response = {'result': True}
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def test_logged_in(request):
    response = {'result': False, 'reason': 'nope'}
    user = is_logged_in(request)
    if user:
        response['result'] = True
        response['message'] = "Working"
    else:
        response['reason'] = "GET"
    return HttpResponse(json.dumps(response), content_type="application/json")    

@csrf_exempt
def signup(request):
    response = {'result': False, 'reason': 'nope'}
    if request.method == "POST":

        email = request.POST.get('email', '')
        if User.objects.filter(email=email):
            response['reason'] = "Email exists"
            return HttpResponse(json.dumps(response), content_type="application/json")

        # import pdb
        # pdb.set_trace()
        try:
            user = User.objects.create(first_name=request.POST['first_name'],
                                last_name = request.POST['last_name'],
                                gender = request.POST['gender'],
                                email = request.POST['email'])

            response['result'] = True
            response['message'] = "Signed up"
            response['pk'] = user.pk
            response['key1'] = user.key1
            response['key2'] = user.key2
        except:
            response['reason'] = "Incomplete Data"
    else:
        response['reason'] = "GET"

    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def get_person_details(request, pk):
    response = {'result': False, 'reason': 'nope'}
    # import pdb
    # pdb.set_trace()
    user = is_logged_in(request)
    if user:
        person = User.objects.filter(pk=pk)
        if person:
            person = person[0]

            groups = [{"name": x.name, 'pk': x.pk} for x in person.groups.all()]
            badges = [{"name": x.name} for x in person.badges.all()]
            tasks = [{"group": {"name":x.group.first().name, "pk":x.group.first().pk}, "pk": x.pk} for x in person.tasks.all()]
            adminOf = [{"name": x.name, "pk": x.pk} for x in person.adminOf.all()]
            posts = [{"description": x.description} for x in person.posts.all()]

            response['result'] = True
            response['data'] = {
                    "first_name": person.first_name,
                    "last_name": person.last_name,
                    "gender": person.gender,
                    "groups": groups,
                    "badges": badges,
                    "tasks": tasks,
                    "adminOf": adminOf,
                    "posts": posts
                }
        response['reason'] = "No person with this pk"
    else:
        response['reason'] = "not logged in"
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def create_group(request):
    response = {'result': False, 'reason': 'nope'}
    # import pdb
    # pdb.set_trace()
    user = is_logged_in(request)
    if user:
        try:
            group = Group.objects.create(name=request.POST['name'],
                description=request.POST['description'], private=request.POST['private'])
            user.groups.add(group)
            user.adminOf.add(group)
            user.save()
            response['result'] = True
            response['message'] = "Group created"
            response['data'] = {
                "pk": group.pk,
                "code": group.joining_code
            }
        except:
            response['reason'] = "Most probably incomplete data"
    else:
        response['reason'] = "not logged in"
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def get_group_details(request, pk):
    response = {'result': False, 'reason': 'nope'}
    # import pdb
    # pdb.set_trace()
    user = is_logged_in(request)
    if user:
        group = Group.objects.filter(pk=pk)
        if group:
            group = group[0]
            posts = [{"description": x.description, "pk": x.pk} for x in group.posts.all()]
            tasks = [{"description": x.description, "pk": x.pk} for x in group.tasks.all()]
            members = [{"name": x.full_name(), "pk": x.pk} for x in group.members.all()]
            admins = [{"name": x.full_name(), "pk": x.pk} for x in group.admins.all()]
            response['data'] = {
                "name": group.name,
                "description": group.description,
                "pk": group.pk,
                "posts": posts,
                "tasks": tasks,
                "members": members,
                "admins": admins,
            }
            response['result'] = True
        else:
            response['reason'] = "No Group with this  PK found"
    else:
        response['reason'] = "not logged in"
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def delete_group(request, pk):
    response = {'result': False, 'reason': 'nope'}
    # import pdb
    # pdb.set_trace()
    user = is_logged_in(request)
    if user:
        group = Group.objects.filter(pk=pk)
        if group:
            group = group[0]
            if user in group.admins.all():
                for x in group.posts.all(): x.delete()
                for x in group.tasks.all(): x.delete()
                
                group.delete()
                response['result'] = True
                response['message'] = "Deleted"
            else:
                response['message'] = "You are not an admin"

        else:
            response['reason'] = "No Group with this  PK found"
    else:
        response['reason'] = "not logged in"
    return HttpResponse(json.dumps(response), content_type="application/json")


@csrf_exempt
def join_group(request, pk):
    response = {'result': False, 'reason': 'nope'}
    # import pdb
    # pdb.set_trace()
    user = is_logged_in(request)
    if user:
        group = Group.objects.filter(pk=pk)
        if group:
            group = group[0]
            group.members.add(user)
            group.save()
            response['result'] = True
            response['message'] = "Welcome to %s"%group.name
        else:
            response['reason'] = "No Group with this  PK found"
    else:
        response['reason'] = "not logged in"
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def leave_group(request, pk):
    response = {'result': False, 'reason': 'nope'}
    # import pdb
    # pdb.set_trace()
    user = is_logged_in(request)
    if user:
        group = Group.objects.filter(pk=pk)
        if group:
            group = group[0]
            if user in group.members.all():
                group.members.remove(user)
                group.save()
                user.save()
                response['result'] = True
                response['message'] = "Removed from group"
            else:
                response['reason'] = "You were not a part of the group"
        else:
            response['reason'] = "No Group with this  PK found"
    else:
        response['reason'] = "not logged in"
    return HttpResponse(json.dumps(response), content_type="application/json")



@csrf_exempt
def create_new_post(request, group_pk):
    response = {'result': False, 'reason': 'nope'}
    # import pdb
    # pdb.set_trace()
    user = is_logged_in(request)
    if user:
        group = Group.objects.filter(pk=group_pk)
        if group:
            group = group[0]
            try:
                post = Post.objects.create(description=request.POST['description'])
                post.OP.add(user)
                post.save()
                group.posts.add(post)
                group.save()
                response['result']=True
                response['message'] = "Posted"
                response['data'] = {"pk": post.pk}
            except:
                response['reason'] = "Incomplete Data"

        else:
            response['reason'] = "No Group with this  PK found"
    else:
        response['reason'] = "not logged in"
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def get_post_details(request, pk):
    response = {'result': False, 'reason': 'nope'}
    # import pdb
    # pdb.set_trace()
    user = is_logged_in(request)
    if user:
        post = Post.objects.filter(pk=pk)
        if post:
            post = post[0]
            response['result'] = True
            response['data'] = {
                "group": {
                        "pk":post.group.first().pk,
                        "name": post.group.first().name
                        },
                "pk": post.pk,
                "description": post.description,
                "OP": {
                        "pk": post.OP.first().pk,
                        "name": post.OP.first().full_name()
                }
            }
        else:
            response['reason'] = "No post with this PK found"
    else:
        response['reason'] = "not logged in"
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def delete_post(request, pk):
    response = {'result': False, 'reason': 'nope'}
    import pdb
    pdb.set_trace()
    user = is_logged_in(request)
    if user:
        post = Post.objects.filter(pk=pk)
        if post:
            post = post[0]
            if (user in post.OP.all()) or (user in post.group.first().admins.all()):
                response['result'] = True
                response['message'] = "Deleted"
                post.delete()
            else:
                response['reason'] = "You did not post this or you are not an admin of this group"
        else:
            response['reason'] = "No post with this PK found"
    else:
        response['reason'] = "not logged in"
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def create_task(request, group_pk, person_pk):
    response = {'result': False, 'reason': 'nope'}
    # import pdb
    # pdb.set_trace()
    user = is_logged_in(request)
    if user:
        group = Group.objects.filter(pk=group_pk)
        person = User.objects.filter(pk=person_pk)
        if person and group:
            person, group = person[0], group[0]
            if all([x in group.members.all() for x in [person, user]]):
                try:
                    task = Task.objects.create(description=request.POST['description'])
                    task.assignedto.add(person)
                    task.assigner.add(user)
                    group.tasks.add(task)
                    task.save()
                    person.save()
                    user.save()
                    group.save()
                    response['result'] = True
                    response['message'] = "Task added"
                    response['data'] = {
                                    "pk": task.pk,
                    };
                except:
                    response['reason'] = "Insufficent data"
            else:
                response['reason'] = "You or the other person doesn't belong to this group."
        else:
            response['reason'] = "Group or person with this pk does not exist"
    else:
        response['reason'] = "not logged in"
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def get_task_details(request, pk):
    response = {'result': False, 'reason': 'nope'}
    # import pdb
    # pdb.set_trace()
    user = is_logged_in(request)
    if user:
        task = Task.objects.filter(pk=pk)
        if task:
            task = task[0]
            response['result'] = True
            response['data'] = {
                            "pk": task.pk,
                            "description": task.description,
                            "assigner": {
                                    "name": task.assigner.first().full_name(),
                                    "pk": task.assigner.first().pk
                                    },
                            "assignedto": {
                                    "name": task.assignedto.first().full_name(),
                                    "pk": task.assignedto.first().pk
                            },
                            "group": {
                                    "name": task.group.first().name,
                                    "pk": task.group.first().pk,
                            }
            }
        else:
            response['reason'] = "Task with this pk does not exist"
    else:
        response['reason'] = "not logged in"
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def delete_task(request, pk):
    response = {'result': False, 'reason': 'nope'}
    # import pdb
    # pdb.set_trace()
    user = is_logged_in(request)
    if user:
        task = Task.objects.filter(pk=pk)
        if task:
            task = task[0]
            if user in task.assigner.all():
                task.delete()
                response['result']= True
                response['message'] = "task deleted"
            else:
                response['reason'] = "You did not start this task."
        else:
            response['reason'] = "Task with this pk does not exist"
    else:
        response['reason'] = "not logged in"
    return HttpResponse(json.dumps(response), content_type="application/json")
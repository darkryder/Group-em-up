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
            badges = [{"name": x.name, "points": x.points} for x in person.badges.all()]
            takentasks = [{"group": {"name":x.group.first().name, "pk":x.group.first().pk}, "pk": x.pk, "description": x.description} for x in person.tasks.all()]
            tasksIAssigned = [{"group": {"name":x.group.first().name, "pk":x.group.first().pk}, "pk": x.pk, "description": x.description} for x in person.tasksIAssigned.all()]
            completedtasks = [{"group": {"name":x.group.first().name, "pk":x.group.first().pk}, "pk": x.pk, "description": x.description} for x in person.completedtasks.all()]
            adminOf = [{"name": x.name, "pk": x.pk} for x in person.adminOf.all()]
            posts = [{"description": x.description} for x in person.posts.all()]

            response['result'] = True
            response['data'] = {
                    "first_name": person.first_name,
                    "last_name": person.last_name,
                    "points": person.points,
                    "gender": person.gender,
                    "groups": groups,
                    "badges": badges,
                    "takentasks": takentasks,
                    "tasksIAssigned": tasksIAssigned,
                    "completedtasks": completedtasks,
                    "adminOf": adminOf,
                    "posts": posts
                }
        else:
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
                description=request.POST['description'], private=request.POST.get('private', False))
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
            for i,task in enumerate(group.tasks.all()):
                tasks[i]['completedby'] = {"name": task.completedby.first().full_name(), "pk": tasks.completedby.first().full_name()} if \
                                            task.completedby.all() else None

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
                "points": sum([x.points for x in group.tasks.all()])
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

            badge = Badge.get_baby_steps_badge()
            if badge not in user.badges.all():
                user.badges.add(badge)
                user.points += badge.points
                user.save()
                badge.save()

            badge = Badge.get_social_climber_badge()
            if user.groups.count() >= 5:
                if badge not in user.badges.all():
                    user.badges.add(badge)
                    user.points += badge.points
                    user.save()
                    badge.save()


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
            if user in group.admins.all():
                request['reason'] = "You are an admin. You can't exit the group"
                return HttpResponse(json.dumps(response), content_type="application/json")

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
def assign_admin(request, group_pk, person_pk):
    response = {'result': False, 'reason': 'nope'}
    # import pdb
    # pdb.set_trace()
    user = is_logged_in(request)
    if user:
        group = Group.objects.filter(pk=group_pk)
        person = User.objects.filter(pk=person_pk)

        if group and person:
            group, person = group[0], person[0]

            if user not in group.admins.all():
                response['reason'] = "You don't have permission to perform this action"
                return HttpResponse(json.dumps(response), content_type="application/json")
            
            if not person in group.members.all():
                response['reason'] = "The person should be a member of this group"
                return HttpResponse(json.dumps(response), content_type="application/json")

            if person in group.admins.all():
                response['reason'] = "The person is already an admin of this group"
                return HttpResponse(json.dumps(response), content_type="application/json")

            person.adminOf.add(group)
            person.save()
            group.save()
            response['result'] = True
            response['message'] = "added as admin"

            badge = Badge.get_worth_following_badge()
            if badge not in person.badges.all():
                person.badges.add(badge)
                person.points += badge.points
                person.save()
                badge.save()
        else: 
            response['reason'] = "No group or person with this  PK found"
    else:
        response['reason'] = "not logged in"
    return HttpResponse(json.dumps(response), content_type="application/json")


@csrf_exempt
def remove_admin(request, group_pk, person_pk):
    response = {'result': False, 'reason': 'nope'}
    # import pdb
    # pdb.set_trace()
    user = is_logged_in(request)
    if user:
        group = Group.objects.filter(pk=group_pk)
        person = User.objects.filter(pk=person_pk)

        if group and person:
            group, person = group[0], person[0]

            if user not in group.admins.all():
                response['reason'] = "You don't have permission to perform this action"
                return HttpResponse(json.dumps(response), content_type="application/json")
            
            if not person in group.members.all():
                response['reason'] = "The person should be a member of this group"
                return HttpResponse(json.dumps(response), content_type="application/json")

            if person not in group.admins.all():
                response['reason'] = "The person is already not an admin"
                return HttpResponse(json.dumps(response), content_type="application/json")

            person.adminOf.remove(group)
            person.save()
            group.save()
            response['result'] = True
            response['message'] = "Removed as an admin"
        else: 
            response['reason'] = "No group or person with this  PK found"
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
            if group in user.groups.all(): 
                try:
                    post = Post.objects.create(description=request.POST['description'])
                    post.OP.add(user)
                    post.save()
                    group.posts.add(post)
                    group.save()
                    response['result']=True
                    response['message'] = "Posted"
                    response['data'] = {"pk": post.pk}

                    badge = Badge.get_is_there_anybody_out_there_badge()
                    if badge not in user.badges.all():
                        user.badges.add(badge)
                        user.points += badge.points
                        user.save()
                        badge.save()

                except:
                    response['reason'] = "Incomplete Data"
            else:
                response['reason'] = "you are not a member of this group"
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
    # import pdb
    # pdb.set_trace()
    user = is_logged_in(request)
    if user:
        post = Post.objects.filter(pk=pk)
        if post:
            post = post[0]
            if (user in post.group.first().admins.all()) or (user in post.OP.all()):
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
def create_task(request, group_pk):
    response = {'result': False, 'reason': 'nope'}
    # import pdb
    # pdb.set_trace()
    user = is_logged_in(request)
    if user:
        group = Group.objects.filter(pk=group_pk)
        if group:
            group = group[0]
            if user not in group.admins.all():
                response['reason'] = "You're not an admin of this group"
                return HttpResponse(json.dumps(response), content_type="application/json")
            try:
                if 0 > int(request.POST.get('points', 1)) < 100:
                    response['reason'] = "You must allot between 0 and 100 points"
                    return HttpResponse(json.dumps(response), content_type="application/json")    

                task = Task.objects.create(description=request.POST['description'],
                        points = int(request.POST.get('points', 10)))
                task.assigner.add(user)
                group.tasks.add(task)
                task.save()
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
            response['reason'] = "Group with this pk does not exist"
    else:
        response['reason'] = "not logged in"
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def create_task_specific_to_person(request, group_pk, person_pk):
    response = {'result': False, 'reason': 'nope'}
    # import pdb
    # pdb.set_trace()
    user = is_logged_in(request)
    if user.pk == int(person_pk):
        response['reason'] = "You can't assign a task to yourself"
        return HttpResponse(json.dumps(response), content_type="application/json")
    if user:
        group = Group.objects.filter(pk=group_pk)
        person = User.objects.filter(pk=person_pk)
        if person and group:
            person, group = person[0], group[0]
            if user not in group.admins.all():
                response['reason'] = "You're not an admin of this group"
                return HttpResponse(json.dumps(response), content_type="application/json")
            if all([x in group.members.all() for x in [person, user]]):
                try:
                    task = Task.objects.create(description=request.POST['description'],
                        points = int(request.POST.get('points', 10)))
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
                            "assignedto": [{
                                    "name": x.full_name(),
                                    "pk": x.pk
                            } for x in task.assignedto.all()],
                            "group": {
                                    "name": task.group.first().name,
                                    "pk": task.group.first().pk,
                            },
                            "points": task.points,
            }
            response['data']['completedby'] = {"name": task.completedby.first().full_name(), "pk": task.completedby.first().pk} if \
                                                task.completedby.all() else None
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
            if (user in task.assigner.all()) or (user in task.group.first().admins.all()):
                for x in task.completedby.all():
                    x.points -= task.points
                    x.save()

                task.delete()

                response['result']= True
                response['message'] = "task deleted"
            else:
                response['reason'] = "You did not start this task and you are not an admin."
        else:
            response['reason'] = "Task with this pk does not exist"
    else:
        response['reason'] = "not logged in"
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def accept_task(request, pk):
    response = {'result': False, 'reason': 'nope'}
    # import pdb
    # pdb.set_trace()
    user = is_logged_in(request)
    if user:
        task = Task.objects.filter(pk=pk)
        if task:
            task = task[0]
            if not task.group.first() in user.groups.all():
                response['reason'] = "You're not a part of the group that this task is of"
                return HttpResponse(json.dumps(response), content_type="application/json")

            task.assignedto.add(user)
            task.save()
            user.save()
            response['result'] = True
            response['message'] = "Added task"
        else:
            response['reason'] = "Task with this pk does not exist"
    else:
        response['reason'] = "not logged in"
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def reject_task(request, pk):
    response = {'result': False, 'reason': 'nope'}
    # import pdb
    # pdb.set_trace()
    user = is_logged_in(request)
    if user:
        task = Task.objects.filter(pk=pk)
        if task:
            task = task[0]
            if not user in task.assignedto.all():
                response['reason'] = "You were never assigned to this task"
                return HttpResponse(json.dumps(response), content_type="application/json")

            task.assignedto.remove(user)
            task.save()
            user.save()
            response['result'] = True
            response['message'] = "Removed from task"
        else:
            response['reason'] = "Task with this pk does not exist"
    else:
        response['reason'] = "not logged in"
    return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def complete_task(request, pk, person_pk):
    response = {'result': False, 'reason': 'nope'}
    # import pdb
    # pdb.set_trace()
    user = is_logged_in(request)
    if user:
        task = Task.objects.filter(pk=pk)
        person = User.objects.filter(pk=person_pk)
        if task and person:
            task, person = task[0], person[0]
            if not (user in task.assigner.all() or user in task.group.first().admins.all()):
                response['reason'] = "You don't have permission to mark it complete"
                return HttpResponse(json.dumps(response), content_type="application/json")
            if person in task.assignedto.all():
                task.completedby.add(person)
                task.save()
                person.points += task.points
                person.save()
                response['result'] = True
                response['message'] = "Done"

                badge = Badge.get_well_begun_is_half_done_badge()
                if badge not in person.badges.all():
                    person.badges.add(badge)
                    person.points += badge.points
                    person.save()
                    badge.save()

                if person.completedtasks.count() > 10:
                    badge = Badge.get_dependable_badge()
                    if badge not in person.badges.all():
                        person.badges.add(badge)
                        person.points += badge.points
                        person.save()
                        badge.save()
            else:
                response['reason'] = "This person was never assigned this task"
        else:
            response['reason'] = "Task with this pk does not exist"
    else:
        response['reason'] = "not logged in"
    return HttpResponse(json.dumps(response), content_type="application/json")

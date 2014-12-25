from django.db import models

# Create your models here.

class Task(models.Model):
	description = models.CharField(max_length=3000, blank=False)
	assigner = models.ManyToManyField('User', blank=False, null=True)

	def isassigner(this, user):
		return this.assigner == user
	def isassignee(this, user):
		return (this.assignedto == user) or (this.assignedto in user)

class Post(models.Model):
	description = models.CharField(max_length=1024)

def generate_code(q):
	import string
	import random
	temp = []
	temp.extend(string.digits)
	temp.extend(string.letters)
	value = []
	for _ in xrange(q):
		value.append(random.choice(temp))
	return ''.join(value)

class Group(models.Model):
	posts = models.ManyToManyField(Post, related_name='group', null=True)
	tasks = models.ManyToManyField(Task, related_name='group', null=True)
	name = models.CharField(max_length=2000, blank=False)
	description = models.CharField(max_length=4000, blank=False)
	private = models.BooleanField(default=False)
	joining_code = models.CharField(max_length=8, blank=False, default=generate_code(8))

	def change_joining_code(self):
		self.joining_code = generate_code(8)
		self.save()

class Badge(models.Model):
	name = models.CharField(max_length=32)

	@staticmethod
	def first_badge():
		return Badge.objects.get(pk=1)

	@staticmethod
	def second_badge():
		return Badge.objects.get(pk=2)

	@staticmethod
	def third_badge():
		return Badge.objects.get(pk=3)

	@staticmethod
	def fourth_badge():
		return Badge.objects.get(pk=4)

	@staticmethod
	def fifth_badge():
		return Badge.objects.get(pk=5)

	@staticmethod
	def sixth_badge():
		return Badge.objects.get(pk=6)


class User(models.Model):
	first_name = models.CharField(max_length=128, blank=False)
	last_name = models.CharField(max_length=128, blank=False)
	gender = models.BooleanField(default = True) # True is female. false is male
	groups = models.ManyToManyField(Group, related_name='members', null=True)
	badges = models.ManyToManyField(Badge, related_name='people', null=True)
	tasks = models.ManyToManyField(Task, related_name='assignedto', null=True)
	adminOf = models.ManyToManyField(Group, related_name='admins', null=True)
	posts = models.ManyToManyField(Post, related_name='OP', null=True)
	email = models.CharField(max_length=1000, blank=False)

	key1 = models.CharField(max_length=32, default=generate_code(32))
	key2 = models.CharField(max_length=32, default=generate_code(32))

	def full_name(self):
		return ' '.join([self.first_name, self.last_name])

	def name(self):
		return self.full_name


class ForgotPasswordRequest(models.Model):
	key1 = models.CharField(max_length=32, default=generate_code(32))
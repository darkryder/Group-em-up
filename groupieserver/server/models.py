from django.db import models
from django.core.exceptions import ObjectDoesNotExist


# Create your models here.

class Task(models.Model):
	description = models.CharField(max_length=3000, blank=False)
	assigner = models.ManyToManyField('User', blank=False, null=True, related_name='tasksIAssigned')
	points = models.IntegerField(max_length=2, blank=False, default=10)
	completedby = models.ManyToManyField('User', blank=True, null=True, related_name='completedtasks')

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
	joining_code = models.CharField(max_length=8, blank=False, default=lambda:generate_code(8))

	def change_joining_code(self):
		self.joining_code = generate_code(8)
		self.save()

class Badge(models.Model):
	name = models.CharField(max_length=32)
	points = models.IntegerField(max_length=2, blank=False, default=10)

	# when you join your first group
	@staticmethod
	def get_baby_steps_badge():
		try:
			return Badge.objects.get(name='Baby steps')
		except ObjectDoesNotExist:
			badge = Badge.objects.create(name='Baby steps', points=10)
			return badge

	# when you first post something on the group
	@staticmethod
	def get_is_there_anybody_out_there_badge():
		try:
			return Badge.objects.get(name='Is there anybody out there?')
		except ObjectDoesNotExist:
			badge = Badge.objects.create(name='Is there anybody out there?', points=20)
			return badge

	# when you complete your first task
	@staticmethod
	def get_well_begun_is_half_done_badge():
		try:
			return Badge.objects.get(name='Well begun is half done')
		except ObjectDoesNotExist:
			badge = Badge.objects.create(name='Well begun is half done', points=25)
			return badge

	# when you join 5 groups
	@staticmethod
	def get_social_climber_badge():
		try:
			return Badge.objects.get(name='Social climber')
		except ObjectDoesNotExist:
			badge = Badge.objects.create(name='Social climber', points=50)
			return badge

	# when you complete 10 tasks
	@staticmethod
	def get_dependable_badge():
		try:
			return Badge.objects.get(name='Dependable')
		except ObjectDoesNotExist:
			badge = Badge.objects.create(name='Dependable', points=250)
			return badge

	# when you first become an admin
	@staticmethod
	def get_worth_following_badge():
		try:
			return Badge.objects.get(name='Worth following')
		except ObjectDoesNotExist:
			badge = Badge.objects.create(name='Worth following', points=100)
			return badge

	# when you first appear on the leaderboard
	@staticmethod
	def get_starstruck_badge():
		try:
			return Badge.objects.get(name='Starstruck')
		except ObjectDoesNotExist:
			badge = Badge.objects.create(name='Starstruck', points=200)
			return badge


class User(models.Model):
	first_name = models.CharField(max_length=128, blank=False)
	last_name = models.CharField(max_length=128, blank=False)
	points = models.IntegerField(max_length=2, blank=False, default=0)
	gender = models.BooleanField(default = True) # True is female. false is male
	groups = models.ManyToManyField(Group, related_name='members', null=True)
	badges = models.ManyToManyField(Badge, related_name='people', null=True)
	tasks = models.ManyToManyField(Task, related_name='assignedto', null=True)
	adminOf = models.ManyToManyField(Group, related_name='admins', null=True)
	posts = models.ManyToManyField(Post, related_name='OP', null=True)
	email = models.CharField(max_length=1000, blank=False)

	key1 = models.CharField(max_length=32, default=lambda: generate_code(32))
	key2 = models.CharField(max_length=32, default=lambda: generate_code(32))

	def full_name(self):
		return ' '.join([self.first_name, self.last_name])

	def name(self):
		return self.full_name


class ForgotPasswordRequest(models.Model):
	key1 = models.CharField(max_length=32, default=lambda: generate_code(32))
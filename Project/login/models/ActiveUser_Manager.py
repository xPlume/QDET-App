from django.db import models

"""
To use this class, place the following line
objects = ActiveUserManager(user_field='user_field')
on models which contain a foreign key to User,
where 'user_field' is the attribute containing the ForeignKey
"""


class ActiveUserQuerySet(models.QuerySet):
	
	
	def for_active_users(self, user_field):
		"""Filters the queryset based on the related user's active status."""
		lookup = {f"{user_field}__is_active": True}
		return self.filter(**lookup)
	#def 
	
#class


class ActiveUserManager(models.Manager):
	
	
	def __init__(self, user_field='user', *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.user_field = user_field
	#def
	
	
	def get_queryset(self):
		# By default, only return objects with active users
		return ActiveUserQuerySet(self.model, using=self._db).for_active_users(self.user_field)
	#def
	
#class
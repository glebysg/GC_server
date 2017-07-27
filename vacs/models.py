# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.encoding import python_2_unicode_compatible
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role
import collections
import random, string
import json
from django.conf import settings
import yagmail


########################################
##############  GLOBALS  ###############
########################################
command_code = {
    1:2,
    2:2,
    3:2,
    4:2,
    5:4,
    6:4,
    7:2,
    8:2,
    9:2,
    10:4,
    11:2,
}

########################################
############## FUNCTIONS ###############
########################################
def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

def create_replication():
    random_groups = range(1,12)
    random.shuffle(random_groups)
    random_commands = []
    for index in random_groups:
        sub_commands = range(1,command_code[index]+1)
        random.shuffle(sub_commands)
        commands = [{ 'code': str(index) + '_'+str(sc), \
                      'pk': -1} for sc in sub_commands]
        random_commands.append(commands)
    return random_commands



########################################
##############  MODELS   ###############
########################################

class Experiment(models.Model):
    name = models.CharField(max_length=200)
    student_n = models.IntegerField(default=0,
            validators=[MinValueValidator(0)])
    expert_n = models.IntegerField(default=0,
            validators=[MinValueValidator(0)])
    student_cmd_n  = models.IntegerField(default=2,
            validators=[MinValueValidator(2)])
    expert_cmd_n  = models.IntegerField(default=1,
            validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)
    in_validation = models.BooleanField(default=False)
    replications = models.TextField(blank=True)
    owner = models.ForeignKey(User)

class Vac(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='vacs')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

class Command(models.Model):
    name = models.CharField(unique=True, max_length=200)
    code = models.CharField(unique=True, max_length=4)

class Score(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    vac = models.ForeignKey(Vac, on_delete=models.CASCADE)
    command = models.ForeignKey(Command, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)

class Assignment(models.Model):
    command = models.ForeignKey(Command, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lexicon_order = models.CharField(max_length=200)
    current_comparison = models.IntegerField(default=0,
            validators=[MinValueValidator(0),
	    MaxValueValidator(15)])
    current_vac = models.ForeignKey(Vac,
	on_delete=models.CASCADE, null=True, blank=True,
        related_name='current_assigned')
    evaluated_vacs = models.ManyToManyField(Vac, blank=True,
            related_name='evaluated_assigned')
    done = models.BooleanField(default=False)

class Evaluation(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    vac = models.ForeignKey(Vac, on_delete=models.CASCADE)
    evaluation = models.CharField(default="empty", max_length=100)
    number = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    # unique_together = ("assignment","number","vac")


########################################
##############  SIGNALS  ###############
########################################
@receiver(post_save, sender=Experiment)
def model_post_save(sender, instance, created,**kwargs):
    if created:
	exp_key = instance.pk
	subj_count = 1
	user_list = []
	password_list = []
        print instance

	# Create students and experts
	for i in range(instance.expert_n):
	    username = 'e'+str(exp_key)+'_e'+str(i+1)
	    user = User.objects.create_user(
		    username=username,
		    email="example@example.com")
	    password = randomword(4)
	    user.set_password(password)
	    user.save()
	    new_user = User.objects.get(username=username)
	    assign_role(new_user, 'expert')
	    subj_count += 1
	    user_list.append(username)
	    password_list.append(password)
            participant = Participant(user=new_user, experiment=instance)
            participant.save()
	    print 'Expert {0} successfully created.'.format(username)
	    print 'Password: '+password

	for i in range(instance.student_n):
	    username = 'e'+str(exp_key)+'_s'+str(i+1)
	    user = User.objects.create_user(
		    username=username,
		    email="example@example.com")
	    password = randomword(4)
	    user.set_password(password)
            user.experiment = instance
	    user.save()
	    new_user = User.objects.get(username=username)
	    assign_role(new_user, 'student')
	    subj_count += 1
	    user_list.append(username)
	    password_list.append(password)
            participant = Participant(user=new_user, experiment=instance)
            participant.save()
	    print 'Student {0} successfully created.'.format(username)
	    print 'Password: '+password

	# Create The replications
	replications = [create_replication(),create_replication(),create_replication()]

	# Assign the gestures to the experts
	assigned = 0
	counter = 0
	replication = 0
	user_counter = 0
	total_assignments = instance.expert_n*instance.expert_cmd_n +\
			    instance.student_n*instance.student_cmd_n
        print "ASSIGNING USERS"
        print "Total assignments: ", total_assignments
	while (assigned <total_assignments):
	    user = User.objects.get(
		    username=user_list[user_counter])
	    if has_role(user,'expert'):
		command_n= instance.expert_cmd_n
	    else:
		command_n= instance.student_cmd_n
	    command_counter = 0
	    while(command_counter < command_n):
                print "assigned: " + str(assigned)
                print "user counter: " + str(user_counter)
                print "counter: " + str(counter)
                print "command_counter: " + str(command_counter)
                print "replications: " + str(replication)
                print "***************************************"
                print "***************************************"
		group_index = counter%11
		assignment_created = False
                full_code = replications[replication][group_index][0]['code']
                group_code = int(full_code.split('_')[0])
		for i in range(command_code[group_code]):
		    elem = replications[replication][group_index][i]
		    code = elem['code']
		    pk = elem['pk']
		    # If unassigned, assign it
		    if pk == -1:
                        lexicon_order = range(1,10)
                        random.shuffle(lexicon_order)
                        lexicon_order = ''.join([str(l)+',' for l in lexicon_order])
			command = Command.objects.get(code=code)
			assignment = Assignment.objects.create(
			    command = command,
                            lexicon_order = lexicon_order,
			    user = user)
			assignment.save()
			elem['pk'] = assignment.pk
			assigned += 1
                        command_counter +=1
                        replication = assigned/28
                        break
                counter += 1
	    user_counter += 1
        experiment = Experiment.objects.get(pk=instance.pk)
	experiment.replications = json.dumps(replications)
        print experiment.replications
        experiment.save()

        # Send email to the creator with all the data
        msg = "EXPERTS:\n"
        for index in range(instance.expert_n):
            msg += str(index+1)+") username: "+user_list[index]
            msg += ", password: "+password_list[index]+"\n"
        msg += "__________________________________\n"
        msg += "__________________________________\n"
        msg += "STUDENTS:\n"
        for index in range(instance.student_n):
            msg += str(index+1)+") username: "\
                    +user_list[instance.expert_n+index]
            msg += ", password: "+\
                    password_list[instance.expert_n+index]+"\n"
        yag = yagmail.SMTP(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
        subject = 'Your Experiment ' + instance.name +  ' information'
        to = instance.owner.email
        yag.send(to, subject, msg)
        yag.send('glebysg@gmail.com', subject, msg)

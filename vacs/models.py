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
        commands = [{ 'code': str(index) + '.'+str(sc), \
                      'pk': -1} for sc in sub_commands]
        random_commands.append(commands)
    print random_commands
    return random_commands


def send_email(recipient, subject, body):
    import smtplib

    gmail_user = 'isat.gestureclean@gmail.com'
    gmail_pwd = 'bdrtcjoybsmmieke'
    FROM = 'isat.gestureclean@gmail.com'
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"

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
    replications = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict},
            blank=True)
    owner = models.ForeignKey(User)

class Vacs(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)

class Vac(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

class Evaluation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    vac = models.ForeignKey(Vac, on_delete=models.CASCADE)
    evaluation = models.CharField(max_length=100)

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
    current_lexicon = models.IntegerField(default=1,
            validators=[MinValueValidator(1), MaxValueValidator(9)])
    done = models.BooleanField(default=False)


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
	    username = 'e'+str(exp_key)+'_s'+str(subj_count)
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
	    username = 'e'+str(exp_key)+'_s'+str(subj_count)
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
	while (assigned <total_assignments):
	    user = User.objects.get(
		    username=user_list[user_counter])
	    if has_role(user,'expert'):
		command_n= instance.expert_cmd_n
	    else:
		command_n= instance.student_cmd_n
	    command_counter = 0
	    while(command_counter < command_n):
		group_index = counter%11
		assignment_created = False
                full_code = replications[replication][group_index][0]['code']
                group_code = int(full_code.split('.')[0])
		for i in range(command_code[group_code]):
		    elem = replications[replication][group_index][i]
		    code = elem['code']
		    pk = elem['pk']
		    # If unassigned, assign it
		    if pk == -1:
			command = Command.objects.get(code=code)
			assignment = Assignment.objects.create(
			    command = command,
			    user = user)
			assignment.save()
			elem['pk'] = assignment.pk
			assigned += 1
                        command_counter +=1
			assignment_created = True
                        break
                counter += 1
	    user_counter += 1
	    replication = assigned/28
	instance.replication = json.dumps(replications)
	instance.save()

	# Send email to the creator with all the data

        print instance.owner.email
        send_email(
            instance.owner.email,
            'Your Experiment ' + instance.name +  ' information',
            'Here is the message.',
        )

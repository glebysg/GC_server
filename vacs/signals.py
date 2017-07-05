from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
from vacs.models import Experiment, Assignment, Command
import random, string
import json

def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))
def create_replication():
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
        11:2
    }
    random_groups = range(1,12)
    shuffle(random_groups)
    random_commands = []
    for index in random_groups:
        sub_commands = range(1,command_code[index]+1)
        shuffle(commands)
        commands = [{ 'code': str(index) + '.'+str(sc), \
                      'pk': -1} for cd in sub_commands]
        random_commands.append(commands)
    return random_commands

@receiver(post_save, sender=Experiment)
def model_post_save(sender, instance, created,**kwargs):
    if created:
        exp_key = instance.pk
        subj_count = 1
        user_list = []
        password_list = []

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
            print 'Expert {0} successfully created.'.format(username)
            print 'Password: '+password

        for i in range(instance.student_n):
            username = 'e'+str(exp_key)+'_s'+str(subj_count)
            user = User.objects.create_user(
                    username=username,
                    email="example@example.com")
            password = randomword(4)
            user.set_password(password)
            user.save()
            new_user = User.objects.get(username=username)
            assign_role(new_user, 'student')
            subj_count += 1
            user_list.append(username)
            password_list.append(password)
            print 'Student {0} successfully created.'.format(username)
            print 'Password: '+password

        # Create The replications
        replications = [create_replication(),create_replication(),create_replication()]

        # Assign the gestures to the experts
        assigned = 0
        counter = 0
        replication = 0
        user_counter = 0
        total_assignments = expert_n*expert_cmd_n +\
                            student_n*student_cmd_n
        while (assigned <total_assignments):
            user = User.objects.get(
                    username=usernames[user_counter])
            if has_role(user,'expert'):
                command_n= expert_cmd_n
            else:
                command_n= student_cmd_n
            command_counter = 0
            while(command_counter < command_n):
                group_index = counter%11
                assignment_created = False
                for i in range(command_code[group_index]):
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
                        elem[i]['pk'] = assignment.pk
                        assigned += 1
                        assignment_created = True
                counter += 1
                if assignment_created:
                    command_counter +=1
            user_counter += 1
            replication = assigned/28
        instance.replication = json.dumps(replications)
        instance.save()

        # Send email to the creator with all the data


        # Write everything in a file too


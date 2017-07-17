import sys
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rolepermissions.roles import assign_role
from vacs.models import Command

User = get_user_model()

# CREATE USERS
#  Each tuple represents the username, password, and email of a user.
users = [
    ('glebys', 'isatlab', 'gonza337@purdue.edu'),
    ('naveen', 'isatlab', 'nmadapan@purdue.edu'),
    ('juan', 'isatlab', 'jpwachs@purdue.edu'),
    ('lisa', 'utdallas', 'lisa.goffman@utdallas.edu'),
]

for username, password, email in users:
    try:
        print 'Creating user {0}.'.format(username)
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()

        assert authenticate(username=username, password=password)
        print 'User {0} successfully created.'.format(username)
        # Get the user from the database
        new_user = User.objects.get(username=username)
        # Assign Role 
        assign_role(new_user, 'researcher')

    except:
        print 'There was a problem creating the user: {0}.  Error: {1}.' \
            .format(username, sys.exc_info()[1])

# CREATE COMMANDS
# TODO: replicated in /vacs/signals. Need to put it in one place
Command.objects.all().delete()
commands=[
    ('1_1', 'Scroll Up'),
    ('1_2', 'Scroll Down'),
    ('2_1', 'Flip Horizontal'),
    ('2_2', 'Flip Vertical'),
    ('3_1', 'Rotate Clockwise'),
    ('3_2', 'Rotate Anti_clockwise'),
    ('4_1', 'Zoom In'),
    ('4_2', 'Zoom Out'),
    ('5_1', 'Switch_panel Left'),
    ('5_2', 'Switch_panel Right'),
    ('5_3', 'Switch_panel Up'),
    ('5_4', 'Switch_panel Down'),
    ('6_1', 'Pan Left'),
    ('6_2', 'Pan Right'),
    ('6_3', 'Pan Up'),
    ('6_4', 'Pan Down'),
    ('7_1', 'Ruler Measure'),
    ('7_2', 'Ruler Delete'),
    ('8_1', 'PIW Open'),
    ('8_2', 'PIW Close'),
    ('9_1', 'Manual_contrast Increase'),
    ('9_2', 'Manual_contrast Decrease'),
    ('10_1', 'Layout One_panel'),
    ('10_2', 'Layout Two_panels'),
    ('10_3', 'Layout Three_panels'),
    ('10_4', 'Layout Four_panels'),
    ('11_1', 'Contrast_presets Stanadard_1'),
    ('11_2', 'Contrast_presets Stanadard_2'),
]

for code, name in commands:
    try:
        print 'Creating Command {0}.'.format(name)
        command = Command.objects.create(code=code, name=name)
        command.save()
        print 'Command {0} successfully created.'.format(name)
    except:
        print 'There was a problem creating the command: {0}.  Error: {1}.' \
            .format(name, sys.exc_info()[1])

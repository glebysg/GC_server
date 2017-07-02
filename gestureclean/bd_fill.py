import sys
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rolepermissions.roles import assign_role

User = get_user_model()

#  Update the users in this list.
#  Each tuple represents the username, password, and email of a user.
users = [
    ('glebys', 'isatlab', 'gonza337@purdue.edu'),
    ('naveen', 'isatlab', 'gonza337@purdue.edu'),
    ('juan', 'isatlab', 'gonza337@purdue.edu'),
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

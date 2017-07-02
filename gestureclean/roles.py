from rolepermissions.roles import AbstractUserRole

class Participant(AbstractUserRole):
    available_permissions = {
        'create_evaluation': True,
        'create_validation': True,
    }

class Researcher(AbstractUserRole):
    available_permissions = {
        'create_experiment': True,
        'edit_experiment': True,
    }

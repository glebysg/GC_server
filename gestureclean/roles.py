from rolepermissions.roles import AbstractUserRole

class Expert(AbstractUserRole):
    available_permissions = {
        'update_evaluation': True,
        'create_validation': True,
    }

class Student(AbstractUserRole):
    available_permissions = {
        'update_evaluation': True,
        'create_validation': True,
    }

class Researcher(AbstractUserRole):
    available_permissions = {
        'crud_experiment': True,
    }

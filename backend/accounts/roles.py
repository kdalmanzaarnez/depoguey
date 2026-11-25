# Namen van de Django-groepen die de WMS-rol bepalen.
EMPLOYEE = 'Medewerker'
ADMIN = 'Admin'

ALL_ROLES = [EMPLOYEE, ADMIN]


def get_role(user):
    """Geeft 'admin', 'employee' of None terug voor een ingelogde gebruiker."""
    if not user.is_authenticated:
        return None
    group_names = set(user.groups.values_list('name', flat=True))
    if ADMIN in group_names:
        return 'admin'
    if EMPLOYEE in group_names:
        return 'employee'
    return None

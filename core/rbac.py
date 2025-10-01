from schemas.user import Role, Permission, User

ROLE_PERMISSIONS: dict[Role, list[Permission]] = {
    Role.ADMIN: [
        # Admin has all permissions

        Permission.CREATE_USER,
        Permission.READ_USER,
        Permission.UPDATE_USER,
        Permission.DELETE_USER,
        Permission.MANAGE_ROLES,
        Permission.VIEW_METRICS
    ],
    Role.MANAGER: [
        # Manager can view users

        Permission.READ_USER,
        Permission.VIEW_METRICS
    ],
    Role.USER: [
    ]
}

_user_module = None


def get_permissions_for_role(role):
    """Get tle list pf permissions for a given role."""
    return ROLE_PERMISSIONS.get(role, [])

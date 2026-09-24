from app.models.user import UserRole

# Role hierarchy: higher index = more permission
ROLE_LEVELS = {
    UserRole.viewer: 1,
    UserRole.noc: 2,
    UserRole.engineer: 3,
    UserRole.admin: 4,
}


def has_min_role(user_role: UserRole, min_role: UserRole) -> bool:
    return ROLE_LEVELS.get(user_role, 0) >= ROLE_LEVELS.get(min_role, 0)
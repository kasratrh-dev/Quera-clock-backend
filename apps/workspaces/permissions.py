from .models import WorkspaceMembership


ROLE_RANK = {
    "owner": 3,
    "admin": 2,
    "manager": 2,
    "member": 1,
}


def get_workspace_membership(user, workspace):
    if not user.is_authenticated:
        return None

    return (
        WorkspaceMembership.objects
        .for_user(user)
        .filter(workspace=workspace)
        .first()
    )


def get_workspace_role(user, workspace):
    if not user.is_authenticated:
        return None

    if workspace.owner_id == user.id:
        return "owner"

    membership = get_workspace_membership(user, workspace)

    if membership is None:
        return None

    return membership.role


def has_workspace_role(user, workspace, minimum_role):
    role = get_workspace_role(user, workspace)

    if role is None:
        return False

    return ROLE_RANK[role] >= ROLE_RANK[minimum_role]
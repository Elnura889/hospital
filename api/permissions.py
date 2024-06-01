from rest_framework import permissions
from django.contrib.auth.models import Permission

class DoctorAccessPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        return 'api.view_doctor' in request.user.get_user_permissions()

class RoleBasedPermissionsMixin:
    action_permissions = None

    def get_action_permission(self):
        self.action_permissions = None

    def get_permissions(self):
        self.get_action_permission()
        assert isinstance(self.action_permissions, list), (
                'received a %s'
                % type(self.action_permissions)
        )
        return super().get_permissions()


class HasPermissionByAuthenticatedUserRole(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if len(view.action_permissions) == 0:
                return True
            for permission in view.action_permissions:
                if has_perm(permission, request.user):
                    return True
        return False


def has_perm(perm, user):
    print(get_user_permissions(user))
    return user.is_active and perm in get_user_permissions(user)


def get_user_permissions(user):
    if user.is_superuser:
        return Permission.objects.values_list('codename', flat=True)

    return user.user_permissions.values_list('codename', flat=True) | Permission.objects.filter(
        group__user=user).values_list('codename', flat=True)


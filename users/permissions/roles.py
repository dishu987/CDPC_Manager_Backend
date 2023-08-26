from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class IsHeadPlacementCoordinator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role_group.role == 'HPC' or request.user.role_group.role == 'APC':
            return True
        return False


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role_group.role == 'DPC':
            return True
        return False


class IsStudentCoordinator(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role_group.role == 'Student Coordinator':
            return True
        return False




# New Permissions

class CanAddUsers(permissions.BasePermission):
    # Chairperson/ Vice Chair/ Placement Manager / (HPC) / APC
    def has_permission(self,request,view):
        users_can_create =  ["Chairperson","Vice Chair","Placement Manager","HPC","APC"]
        for user_role in users_can_create:
            if request.user.role_group.role == user_role:
                return True
        # if not in list
        return False
        
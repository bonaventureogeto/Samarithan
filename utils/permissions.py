from rest_framework.permissions import BasePermission


class IsPoliticianAdmin(BasePermission):
    message = "You must be the politician admin to acess this page"

    def has_permission(self, request, view):
        """ check if the object has permission """

        user = request.user

        if user is not None and user.is_authenticated:
            return user.role == 'PA'


class IsAgent(BasePermission):
    message = "you must be an agent to access this endpoint"

    def has_permission(self, request, view):
        """ check if a user is an agent """

        user = request.user

        if user is not None and user.is_authenticated:
            return user.role == 'AG'


class IsCampaignManager(BasePermission):
    """ check if a user is a camapaign manager """

    def has_permission(self, request, view):
        """ check if a user is a campaign manager """

        user = request.user

        if user is not None and user.is_authenticated:
            return user.role == 'CM'


import warnings

from ..model import PersonalPreferences
from .base import Base


class Organization(Base):
    def __init__(self, client):
        super(Organization, self).__init__(client)
        self.client = client

    def find_organization(self, org_name):
        """

        :param org_name:
        :return:
        """
        get_org_path = "/orgs/name/%s" % org_name
        return self.client.GET(get_org_path)

    def get_current_organization(self):
        """

        :return:
        """
        get_current_organization_path = "/org"
        return self.client.GET(get_current_organization_path)

    def create_organization(self, organization):
        """

        :param organization:
        :return:
        """
        create_orgs_path = "/orgs"
        return self.client.POST(create_orgs_path, json={"name": organization["name"]})

    def update_current_organization(self, organization):
        """

        :param organization:
        :return:
        """
        update_current_organization_path = "/org"
        return self.client.PUT(update_current_organization_path, json=organization)

    def get_current_organization_users(self):
        """

        :return:
        """
        get_current_organization_users_path = "/org/users"
        return self.client.GET(get_current_organization_users_path)

    def add_user_current_organization(self, user):
        """

        :param user:
        :return:
        """
        add_user_current_organization_path = "/org/users"
        return self.client.POST(add_user_current_organization_path, json=user)

    def update_user_current_organization(self, user_id, user):
        """

        :param user_id:
        :param user:
        :return:
        """
        update_user_current_organization_path = "/org/users/%s" % user_id
        return self.client.PATCH(update_user_current_organization_path, json=user)

    def delete_user_current_organization(self, user_id):
        """

        :param user_id:
        :return:
        """
        delete_user_current_organization_path = "/org/users/%s" % user_id
        return self.client.DELETE(delete_user_current_organization_path)

    def get_preferences(self):
        """
        Retrieve preferences of current organization.

        :return:
        """
        update_preference = "/org/preferences"
        return self.client.GET(update_preference)

    def update_preferences(self, preferences: PersonalPreferences):
        """
        Update preferences of current organization as a whole.

        From the `preferences` instance, only attributes with values `not None` will be submitted.
        However, Grafana will reset all undefined attributes to its internal defaults.

        If you want to update specific preference attributes, without touching the others,
        please use the `patch_preferences` method.

        :param preferences:
        :return:
        """
        update_preference = "/org/preferences"
        data = preferences.asdict(filter_none=True)

        return self.client.PUT(
            update_preference,
            json=data,
        )

    def patch_preferences(self, preferences: PersonalPreferences):
        """
        Update specific preferences of current organization.

        From the `preferences` instance, only attributes with values `not None` will be submitted
        and updated.

        :param preferences:
        :return:
        """
        update_preference = "/org/preferences"
        data = preferences.asdict(filter_none=True)

        return self.client.PATCH(
            update_preference,
            json=data,
        )


class Organizations(Base):
    def __init__(self, client, api):
        super(Organizations, self).__init__(client)
        self.client = client
        self.api = api

    def update_organization(self, organization_id, organization):
        """

        :param organization_id:
        :param organization:
        :return:
        """
        update_org_path = "/orgs/%s" % organization_id
        return self.client.PUT(update_org_path, json=organization)

    def delete_organization(self, organization_id):
        """

        :param organization_id:
        :return:
        """
        delete_org_path = "/orgs/%s" % organization_id
        return self.client.DELETE(delete_org_path)

    def list_organization(self):
        """

        :return:
        """
        search_org_path = "/orgs"
        return self.client.GET(search_org_path)

    def switch_organization(self, organization_id):
        """

        :param organization_id:
        :return:
        """
        switch_user_organization = "/user/using/%s" % organization_id
        return self.client.POST(switch_user_organization)

    def organization_user_list(self, organization_id):
        """

        :param organization_id:
        :return:
        """
        users_in_org = "/orgs/%s/users" % organization_id
        return self.client.GET(users_in_org)

    def organization_user_add(self, organization_id, user):
        """

        :param organization_id:
        :param user:
        :return:
        """
        add_user_path = "/orgs/%s/users" % organization_id
        return self.client.POST(add_user_path, json=user)

    def organization_user_update(self, organization_id, user_id, user_role):
        """

        :param organization_id:
        :param user_id:
        :param user_role:
        :return:
        """
        patch_user = "/orgs/%s/users/%s" % (organization_id, user_id)
        return self.client.PATCH(patch_user, json={"role": user_role})

    def organization_user_delete(self, organization_id, user_id):
        """

        :param organization_id:
        :param user_id:
        :return:
        """
        delete_user = "/orgs/%s/users/%s" % (organization_id, user_id)
        return self.client.DELETE(delete_user)

    def organization_preference_get(self):
        """
        :return:
        """
        warnings.warn("This method is deprecated, please use `organization.get_preferences`", DeprecationWarning)
        return self.api.organization.get_preferences()

    def organization_preference_update(self, theme="", home_dashboard_id=0, timezone="utc"):
        """

        :param theme:
        :param home_dashboard_id:
        :param timezone:
        :return:
        """
        warnings.warn("This method is deprecated, please use `organization.update_preferences`", DeprecationWarning)
        preferences = PersonalPreferences(theme=theme, homeDashboardId=home_dashboard_id, timezone=timezone)
        return self.api.organization.update_preferences(preferences)

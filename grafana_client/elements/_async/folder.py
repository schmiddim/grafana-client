from ..base import Base


class Folder(Base):
    def __init__(self, client):
        super(Folder, self).__init__(client)
        self.client = client

    async def get_all_folders(self, parent_uid=None):
        """

        :return:
        """
        path = "/folders"
        data = {}
        if parent_uid:
            data["parentUid"] = parent_uid
        return await self.client.GET(path, data=data)

    async def get_folder(self, uid):
        """

        :param uid:
        :return:
        """
        path = "/folders/%s" % uid
        return await self.client.GET(path)

    async def create_folder(self, title, uid=None, parent_uid=None):
        """

        :param title:
        :param uid:
        :param parent_uid:
        :return:
        """
        json_data = dict(title=title)
        if uid is not None:
            json_data["uid"] = uid
        if parent_uid is not None:
            json_data["parentUid"] = parent_uid
        return await self.client.POST("/folders", json=json_data)

    async def move_folder(self, uid, parent_uid):
        """
        Move a folder beneath another parent folder.

        This is relevant only if nested folders are enabled.

        :param uid:
        :param parent_uid:
        :return:
        """
        path = "/folders/%s/move" % uid
        return await self.client.POST(path, json={"parentUid": parent_uid})

    async def update_folder(self, uid, title=None, version=None, overwrite=False, new_uid=None):
        """

        :param uid:
        :param title:
        :param version:
        :param overwrite:
        :param new_uid:
        :return:
        """
        body = {}
        if new_uid:
            body["uid"] = new_uid
        if title:
            body["title"] = title
        if version:
            body["version"] = version
        if overwrite:
            body["overwrite"] = True

        path = "/folders/%s" % uid
        return await self.client.PUT(path, json=body)

    async def delete_folder(self, uid):
        """

        :param uid:
        :return:
        """
        path = "/folders/%s" % uid
        return await self.client.DELETE(path)

    async def get_folder_by_id(self, folder_id):
        """

        :param folder_id:
        :return:
        """
        path = "/folders/id/%s" % folder_id
        return await self.client.GET(path)

    async def get_folder_permissions(self, uid):
        """

        :return:
        """
        path = "/folders/%s/permissions" % uid
        return await self.client.GET(path)

    async def update_folder_permissions(self, uid, items):
        """

        :param uid:
        :param items:
        :return:
        """
        update_folder_permissions_path = "/folders/%s/permissions" % uid
        return await self.client.POST(update_folder_permissions_path, json=items)

    async def update_folder_permissions_for_user(self, uid, user_id, items):
        """

        :param uid:
        :param user_id:
        :param items:
            {"permission": "View"} or {"permission": "Edit"} or {"permission": ""}
        :return:
        """

        update_folder_permissions_path_for_user = "/access-control/folders/%s/users/%s" % (uid, user_id)
        return await self.client.POST(update_folder_permissions_path_for_user, json=items)
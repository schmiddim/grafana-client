from .base import Base


class Health(Base):
    def __init__(self, client):
        super(Health, self).__init__(client)
        self.client = client

    def check(self):
        """

        :return:
        """
        path = "/health"
        return self.client.GET(path)

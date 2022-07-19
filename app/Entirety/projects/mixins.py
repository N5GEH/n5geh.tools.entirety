from django.contrib.auth.mixins import UserPassesTestMixin


class ProjectSelfMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return (
            self.request.user.is_project_admin and obj.owner == self.request.user
        ) or self.request.user.is_server_admin


class ProjectCreateMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_project_admin or self.request.user.is_server_admin

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class ProfessorRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_professor()


class StudentRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_student()

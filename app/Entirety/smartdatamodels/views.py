from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from projects.mixins import ProjectContextMixin, ProjectContextAndViewOnlyMixin
from smartdatamodels.forms import SmartDataModelForm
from smartdatamodels.models import SmartDataModel


class SmartDataModelsList(ProjectContextAndViewOnlyMixin, ListView):
    template_name = "smartdatamodels/smartdatamodels_list.html"
    model = SmartDataModel

    def get_context_data(self, **kwargs):
        context = super(SmartDataModelsList, self).get_context_data(**kwargs)
        context["view_only"] = (
            True
            if self.request.user in self.project.viewers.all()
            and self.request.user not in self.project.maintainers.all()
            and self.request.user not in self.project.users.all()
            and self.request.user is not self.project.owner
            else False
        )
        return context

    def get_queryset(self):
        return SmartDataModel.objects.order_by("date_modified").filter(
            name__icontains=self.request.GET.get("search", default="")
        )


class Create(ProjectContextMixin, CreateView):
    template_name = "smartdatamodels/update.html"
    model = SmartDataModel
    form_class = SmartDataModelForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.last_modified_by = self.request.user
        return super(Create, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "projects:smartdatamodels:list", kwargs={"project_id": self.project.uuid}
        )

    def get(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))


class Update(ProjectContextAndViewOnlyMixin, UpdateView):
    template_name = "smartdatamodels/update.html"
    model = SmartDataModel
    context_object_name = "update_model"
    form_class = SmartDataModelForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.last_modified_by = self.request.user
        return super(Update, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "projects:smartdatamodels:list", kwargs={"project_id": self.project.uuid}
        )

    def get_form_kwargs(self):
        kwargs = super(Update, self).get_form_kwargs()
        view_only = (
            True
            if self.request.user in self.project.viewers.all()
            and self.request.user not in self.project.maintainers.all()
            and self.request.user not in self.project.users.all()
            and self.request.user is not self.project.owner
            else False
        )
        kwargs["view_only"] = view_only
        return kwargs


class Delete(ProjectContextMixin, DeleteView):
    template_name = "smartdatamodels/smartdatamodels_list.html"
    model = SmartDataModel

    def get_success_url(self):
        return reverse_lazy(
            "projects:smartdatamodels:list", kwargs={"project_id": self.project.uuid}
        )

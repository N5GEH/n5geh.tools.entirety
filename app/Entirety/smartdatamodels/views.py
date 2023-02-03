from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from projects.mixins import ProjectContextMixin
from smartdatamodels.forms import SmartDataModelForm
from smartdatamodels.models import SmartDataModel


class SmartDataModelsList(ProjectContextMixin, ListView):
    template_name = "smartdatamodels/smartdatamodels_list.html"
    model = SmartDataModel

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


class Update(ProjectContextMixin, UpdateView):
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


class Delete(ProjectContextMixin, DeleteView):
    template_name = "smartdatamodels/smartdatamodels_list.html"
    model = SmartDataModel

    def get_success_url(self):
        return reverse_lazy(
            "projects:smartdatamodels:list", kwargs={"project_id": self.project.uuid}
        )

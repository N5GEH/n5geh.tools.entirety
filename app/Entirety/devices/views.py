from django.shortcuts import render, redirect
from django.views.generic import View
from django.template import RequestContext
from devices.forms import *

from filip.clients.ngsi_v2 import IoTAClient
from filip.models import FiwareHeader

# TODO for test
IOTA_URL = "http://localhost:4041/"
dummy_project = {"fiware_service": "test", "service_path": "/"}


# Helper functions
def get_device_by_id(current_project, device_id):
    """
    Get device by id for current project
    Args:
        current_project: dict
        device_id: str

    Returns:
        filip.models.ngsi_v2.iot.Device
    """
    with IoTAClient(
        url=IOTA_URL,
        fiware_header=FiwareHeader(
            service=current_project.get("fiware_service"),
            service_path=current_project.get("service_path"),
        ),
    ) as iota_client:
        return iota_client.get_device(device_id=device_id)


def get_devices(current_project):
    """
    Get devices for current project
    Args:
        current_project: dict

    Returns:
        list of devices
    """
    try:
        with IoTAClient(
            url=IOTA_URL,
            fiware_header=FiwareHeader(
                service=current_project.get("fiware_service"),
                service_path=current_project.get("service_path"),
            ),
        ) as iota_client:
            devices = iota_client.get_device_list()
        return devices

    except RuntimeError:
        return [{}]


class DeviceListView(View):
    def get(self, request):
        device_list = get_devices(dummy_project)
        print("receive get request")
        # pass device model of filip directly to context
        context = {"Devices": device_list}
        return render(request, "devices/list.html", context)


class DeviceCreateView(View):
    def get(self, request):
        form = DeviceDetailForm()
        context = {"form": form, "action": "Create"}
        return render(request, "devices/detail.html", context)


class DeviceEditView(View):
    def get(self, request):
        device_id = request.GET["device_id"]
        device = get_device_by_id(dummy_project, device_id=device_id)
        device_dict = device.dict()
        form = DeviceDetailForm(
            initial=device_dict
        )  # the extra fields in dict seem to be ignored
        context = {"form": form, "action": "Edit"}
        return render(request, "devices/detail.html", context)


class DeviceEditSubmitView(View):
    """
    For both creating and updating?
    """

    def post(self, request):
        form = DeviceDetailForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # TODO send update request to IoTa
            return redirect("devices:list")
        else:
            # TODO need another view for create
            form = DeviceDetailForm(request.POST)
            context = {"form": form, "action": "Edit"}
        return render(request, "devices/detail.html", context)

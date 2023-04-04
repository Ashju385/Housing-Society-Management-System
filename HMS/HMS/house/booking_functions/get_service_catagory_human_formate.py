from house.models import Service

def get_service_catagory_human_format(catagory):
    service = Service.objects.all()[0]
    service_catagory = dict(service.SERVICE_CATAGORIES).get(catagory, None)
    return service_catagory

from .availability import check_availability
from house.models import Service

def get_available_services(catagory, check_in, check_out):

    service_list = Service.objects.filter(catagory=catagory)


    available_services=[]

    for service in service_list:
        if check_availability(service,check_in, check_out):
            available_services.append(service)
    
    if len(available_services) > 0:
        return available_services
    else:
        return None
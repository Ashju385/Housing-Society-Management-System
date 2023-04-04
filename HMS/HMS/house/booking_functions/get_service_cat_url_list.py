from django.urls import reverse
from house.models import Service

def get_service_cat_url_list():
    service = Service.objects.all()[0]
    service_catagories = dict(service.SERVICE_CATAGORIES)
    
    
    service_cat_url_list = []
    
    for catagory in service_catagories:
        service_catagory = service_catagories.get(catagory)
        service_url = reverse('house:ServiceDetailView', kwargs={'catagory': catagory})

        service_cat_url_list.append((service_catagory, service_url))

    return service_cat_url_list
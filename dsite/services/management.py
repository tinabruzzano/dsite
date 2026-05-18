SERVICES = []
THIRDY_SERVICES = []

def add_service(service, is_list=False, is_third=False):
    global SERVICES
    global THIRDY_SERVICES

    if is_third:
        if is_list:
            for element in service:
                THIRDY_SERVICES.append(element)
        else:
            THIRDY_SERVICES.append(service)
    else:
        if is_list:
            for element in service:
                SERVICES.append(element)
        else:
            SERVICES.append(service)

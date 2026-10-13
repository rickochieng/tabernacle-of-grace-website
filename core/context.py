from .models import SiteDetails
def site(request):
    return {'site': SiteDetails.load()}

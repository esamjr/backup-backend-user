from .models import BillingLicense


def _qty_license(request):
    return BillingLicense.objects.get(id_company=request)

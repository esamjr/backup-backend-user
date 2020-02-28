from .models import Business


def cek_company_id(request):
    _cek_company = Business.objects.filter(id=request).exists()
    if not _cek_company:
        return False
    return True

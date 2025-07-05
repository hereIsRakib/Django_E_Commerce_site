from .models import Category

def category_list(request):
    cata_list = Category.objects.all()
    return dict(cata_list = cata_list)
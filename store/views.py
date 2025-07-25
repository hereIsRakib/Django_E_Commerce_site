from django.shortcuts import render, get_object_or_404
from category.models import Category
from .models import Product
from cart.models import Cart, CartItem
from cart.views import _cart_id
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
# Create your views here.

def store(request, category_slug = None):

    categories = None
    products = None
    category_name = Category.objects.all()

    if category_slug !=None:
        categories =get_object_or_404(Category, slug = category_slug)
        products = Product.objects.filter(category = categories, is_available = True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()

    else:

        products = Product.objects.all().filter(is_available = True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = Product.objects.count()
        

    context = {
        'category_name': category_name,
        'products' : paged_products,
        'products_count' : products_count,
               }
    return render(request, 'store/store.html',context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug = category_slug, slug = product_slug)
        cart, created = Cart.objects.get_or_create(cart_id = _cart_id(request))
        item_exist_in_cart = CartItem.objects.filter(cart = cart, product = single_product).exists()


    except Exception as e:
         raise e
    
    context = {
        'single_product': single_product,
        'item_exist_in_cart': item_exist_in_cart,
    }

    return render(request, 'store/product_detail.html',context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(product_name__icontains = keyword) | Q(description__icontains = keyword))
            products_count = products.count()
        context = {
            'products': products,
            'products_count': products_count,
        }
        return render(request,'store/store.html/', context)
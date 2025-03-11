from django.shortcuts import render,get_object_or_404

from . models import Category, Product


def store(request):
    all_products = Product.objects.all()
    all_categories = categories(request)
    context = {   
        'my_products':all_products,
        'categories':all_categories['categories']
    }
    return render(request, 'store/store.html',context)
# Create your views here.

# query all data from Category and return them as display

def categories(request):
    return {'categories': Category.objects.all()}

def product_info(request, slug):

    product = get_object_or_404(Product, slug = slug)

    context = {'product':product}

    return render(request,'store/product-info.html',context)

def list_category(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)

    return render(request, 'store/list-category.html', {'category': category, 'products': products})



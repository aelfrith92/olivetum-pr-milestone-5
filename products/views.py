from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import (CreateView, ListView, UpdateView, DeleteView,
                                  View)
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register
from django.db.models.functions import Lower
from .models import Product, Category, Review
from .forms import ProductForm, review_form


@register.filter
def get_range(value):
    return range(value)


@register.filter
def get_range_empty_star(value):
    return range(5-value)


def all_products(request):
    """This view shows/retrieves all products"""

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            queries = (Q(name__icontains=query) |
                       Q(description__icontains=query))
            products = products.filter(queries)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey == 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if sortkey == 'category':
                sortkey = 'category__name'

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request,
                  'products/products.html',
                  context)


class product_detail(View):
    """Overview of a single product"""

    def get(self, request, product_id, *args, **kwargs):
        '''Retrieving related reviews'''

        product = get_object_or_404(Product, pk=product_id)
        reviews = product.reviews.filter(approved=True).order_by('created_on')

        context = {
            'product': product,
            'reviews': reviews,
            'review_form': review_form(),
        }

        return render(request,
                      'products/product_detail.html',
                      context)

    def post(self, request, product_id, *args, **kwargs):
        '''Handling Review submission'''

        product = get_object_or_404(Product, id=product_id)
        reviews = product.reviews.filter(approved=True).order_by('created_on')

        review_dataform = review_form(data=request.POST)

        if review_dataform.is_valid():
            review_dataform.instance.email = request.user.email
            review_dataform.instance.name = request.user.username

            review = review_dataform.save(commit=False)
            review.product = product
            review.save()
        else:
            review_dataform = review_form()

        context = {
            'product': product,
            'reviews': reviews,
            'review_form': review_form(),
        }

        return render(request,
                      'products/product_detail.html',
                      context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the'
                           ' form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure'
                           ' the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))

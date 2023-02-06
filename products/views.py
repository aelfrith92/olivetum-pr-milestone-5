from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import (CreateView, ListView, UpdateView, DeleteView,
                                  View)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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

        reviewed = False

        product = get_object_or_404(Product, pk=product_id)
        staff = request.user.is_staff
        super_u = request.user.is_superuser
        auth_user = request.user.is_authenticated
        if not super_u or not auth_user or not staff:
            reviews = (product.reviews.filter(approved=True)
                       .order_by('created_on'))
        elif super_u or staff:
            reviews = product.reviews.order_by('created_on')

        if request.user.is_authenticated:
            if product.reviews.filter(email=request.user.email).exists():
                reviewed = True

        context = {
            'product': product,
            'reviews': reviews,
            'reviewed': reviewed,
            'review_form': review_form(),
        }

        return render(request,
                      'products/product_detail.html',
                      context)

    def post(self, request, product_id, *args, **kwargs):
        '''Handling Review submission'''

        product = get_object_or_404(Product, id=product_id)
        reviews = product.reviews.filter(approved=True).order_by('created_on')
        reviewed = product.reviews.filter(email=request.user.email).exists()
        review_id_passed = request.POST.get('reviewEditId', False)

        if (reviewed and not review_id_passed):
            messages.info(request, 'You have already left a review for'
                          ' this product.')
        elif (reviewed and review_id_passed):
            review_dataform = review_form(data=request.POST)
            review = get_object_or_404(Review, id=review_id_passed)
            # Enable the following lines for testing purposes
            # print(f'Questi sono i dati dalla post request crudi: '
            #       f'{request.POST}')
            # print(f'This is the form data passed: {review_dataform}')
            # print(f'This is the review that is going to be updated: {review}')

            if review_dataform.is_valid():
                review.body = request.POST['body']
                review.title = request.POST['title']
                review.single_rating = request.POST['single_rating']
                review.save()
            else:
                messages.error(request, 'Failed to add the review. Please'
                               ' ensure the form is valid.')
        else:
            review_dataform = review_form(data=request.POST)

            if review_dataform.is_valid():
                review_dataform.instance.email = request.user.email
                review_dataform.instance.name = request.user.username

                review = review_dataform.save(commit=False)
                review.product = product
                reviewed = True
                review.save()
            else:
                messages.error(request, 'Failed to add the review. Please'
                               ' ensure the form is valid.')

        context = {
            'product': product,
            'reviews': reviews,
            'reviewed': reviewed,
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


@login_required
def delete_review(request, review_id):
    """This view deletes the review"""

    review = get_object_or_404(Review, pk=review_id)
    product_id = review.product.id
    # product = get_object_or_404(Product, pk=product_id)
    review.delete()
    messages.success(request, 'Review deleted!')
    return redirect(reverse('product_detail', args=[product_id]))


@login_required
def hide_review(request, review_id):
    """This view hides the review"""

    review = get_object_or_404(Review, pk=review_id)
    product_id = review.product.id

    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('product_detail', args=[product_id]))

    review.approved = False
    review.save()
    messages.success(request, 'Review hidden!')
    return redirect(reverse('product_detail', args=[product_id]))


@login_required
def unhide_review(request, review_id):
    """This view hides the review"""

    review = get_object_or_404(Review, pk=review_id)
    product_id = review.product.id

    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('product_detail', args=[product_id]))

    review.approved = True
    review.save()
    messages.success(request, 'Review unhidden!')
    return redirect(reverse('product_detail', args=[product_id]))

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import View
from django.http import HttpResponseServerError
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register
from django.db.models.functions import Lower
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Product, Category, Review, Provider, Contact
from checkout.models import Order, OrderLineItem
from .forms import ProductForm, review_form, provider_form


@register.filter
def get_range(value):
    """This filter handles for loop with ranges"""
    return range(value)


@register.filter
def get_range_empty_star(value):
    """
        This filter handles for loop with ranges
        Number of empty stars in the reviews
    """
    return range(5-value)


@register.filter
def get_lat(value):
    return value.split(',')[0]


@register.filter
def get_lon(value):
    return value.split(',')[1]


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

        paginator = Paginator(products, 24)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'page_obj': page_obj,
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

        # The following vars determine the reviews on the
        # front-end, based on the permissions Admin VS standard user
        staff = request.user.is_staff
        super_u = request.user.is_superuser
        auth_user = request.user.is_authenticated
        if super_u or staff:
            reviews = product.reviews.order_by('-created_on')
        else:
            reviews = (product.reviews.filter(approved=True)
                       .order_by('-created_on'))
        # Check whether the user is authenticated
        if auth_user:
            # Check whether the user already left a review about
            # the product on the page
            if product.reviews.filter(email=request.user.email).exists():
                reviewed = True

        # Retrieve all emails on reviews in relation to product_id
        emails_on_reviews = []
        for review in reviews:
            emails_on_reviews.append(review.email)

        # All orders in relation to product_id
        order_line_objects = OrderLineItem.objects.filter(product=product_id)
        emails_on_orders = []
        for order_line_object in order_line_objects:
            order_id = order_line_object.order
            order_object = get_object_or_404(Order, order_number=order_id)
            email_on_order = order_object.email
            emails_on_orders.append(email_on_order)
        verified_reviews = []
        for review_email in emails_on_reviews:
            if review_email in emails_on_orders:
                verified_reviews.append(get_object_or_404(Review,
                                                          email=review_email)
                                        .id)

        context = {
            'product': product,
            'reviews': reviews,
            'reviewed': reviewed,
            'review_form': review_form(),
            'verified_reviews': verified_reviews,
        }

        return render(request,
                      'products/product_detail.html',
                      context)

    def post(self, request, product_id, *args, **kwargs):
        '''Handling Review submission'''

        product = get_object_or_404(Product, id=product_id)

        staff = request.user.is_staff
        super_u = request.user.is_superuser
        auth_user = request.user.is_authenticated
        if super_u or staff:
            reviews = product.reviews.order_by('-created_on')
        else:
            reviews = (product.reviews.filter(approved=True)
                       .order_by('-created_on'))

        reviewed = product.reviews.filter(email=request.user.email).exists()
        review_id_passed = request.POST.get('reviewEditId', False)

        if auth_user:
            if (reviewed and not review_id_passed):
                messages.info(request, 'You have already left a review for'
                                       ' this product.')
            elif (reviewed and review_id_passed):
                review_dataform = review_form(data=request.POST)
                review = get_object_or_404(Review, id=review_id_passed)

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
        # Retrieve all emails on reviews in relation to product_id
        emails_on_reviews = []
        for review in reviews:
            emails_on_reviews.append(review.email)

        # All orders in relation to product_id
        order_line_objects = OrderLineItem.objects.filter(product=product_id)
        emails_on_orders = []
        for order_line_object in order_line_objects:
            order_id = order_line_object.order
            order_object = get_object_or_404(Order, order_number=order_id)
            email_on_order = order_object.email
            emails_on_orders.append(email_on_order)
        verified_reviews = []
        for review_email in emails_on_reviews:
            if review_email in emails_on_orders:
                verified_reviews.append(get_object_or_404(
                    Review, email=review_email).id)

        context = {
            'product': product,
            'reviews': reviews,
            'reviewed': reviewed,
            'review_form': review_form(),
            'verified_reviews': verified_reviews,
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
    if request.user.email is not review.email:
        messages.error(request, 'Sorry, only the review author can do that.')
        return redirect(reverse('product_detail', args=[product_id]))

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


@login_required
def all_providers(request):
    """ Retrieve all providers """
    if not request.user.is_superuser or not request.user.is_staff:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    providers = Provider.objects.all()
    print(providers)
    context = {
        'providers': providers,
    }

    return render(request, 'products/providers.html', context)


@login_required
def add_provider(request):
    """ Add a provider to the store """
    if not request.user.is_superuser or not request.user.is_staff:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = provider_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added provider!')
            return redirect(reverse('all_providers'))
        else:
            messages.error(request, 'Failed to add provider. Please ensure the'
                           ' form is valid.')
    else:
        form = provider_form()

    template = 'products/add_provider.html'
    context = {
        'provider_form': form,
    }

    return render(request, template, context)


@login_required
def edit_provider(request, provider_id):
    """ Edit a product in the store """
    if not request.user.is_superuser or not request.user.is_staff:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    provider = get_object_or_404(Provider, pk=provider_id)
    if request.method == 'POST':
        form = provider_form(request.POST, instance=provider)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated provider!')
            return redirect(reverse('all_providers'))
        else:
            messages.error(request, 'Failed to update product. Please ensure'
                           ' the form is valid.')
    else:
        form = provider_form(instance=provider)
        messages.info(request, f'You are editing {provider.business_name}')

    template = 'products/edit_provider.html'
    context = {
        'form': form,
        'provider': provider,
    }

    return render(request, template, context)


@login_required
def delete_provider(request, provider_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    provider = get_object_or_404(Provider, pk=provider_id)
    provider.delete()
    messages.success(request, 'Provider deleted!')
    return redirect(reverse('all_providers'))


def contactform(request):
    """ Contact form """

    print('view contactform initiated')

    if request.method == 'POST':
        email_from_form = request.POST['contactEmail']
        contactQuery_from_form = request.POST['contactQuery']
        user_is_auth = request.user.is_authenticated
        form_is_from_auth = request.POST.get('authEmail')

        auth_from_form = (form_is_from_auth
                          if user_is_auth else False)

        if auth_from_form and not user_is_auth:
            return HttpResponseServerError(
                render(
                    request,
                    "500.html",
                )
            )

        contact = Contact(
            email=email_from_form,
            query=contactQuery_from_form,
            auth=auth_from_form,
            created_on=datetime.now(),
        )
        contact.save()

        """Send the user a confirmation email"""

        subject = render_to_string(
            '../templates/includes/send_email_confirmation/'
            'confirmation_email_subject.txt',
            {'contact': contact})
        body = render_to_string(
            '../templates/includes/send_email_confirmation/'
            'confirmation_email_body.txt',
            {'contact': contact, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [email_from_form]
        )

    messages.success(
        request, 'Contact request successfully submitted'
    )
    return redirect(reverse('home'))

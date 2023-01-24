from django.shortcuts import (render, redirect, reverse, HttpResponse,
                              get_object_or_404)
from django.contrib import messages
from products.models import Product


def view_bag(request):
    """ A view to return the bag page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None

    if 'product_size' in request.POST:
        """product_size passed via the related input and name attribute"""
        size = request.POST['product_size']  # Then, assign it
    bag = request.session.get('bag', {})  # Now, update the bag session data

    if size:
        """if size has been honoured through the logic above"""
        if item_id in list(bag.keys()):
            """
                if the item_id passed through the request is already among the
                bag session data
            """
            if size in bag[item_id]['items_by_size'].keys():
                """
                    if such item_id found in the bag session data already has a
                    dictionary key named 'size'
                """
                bag[item_id]['items_by_size'][size] += quantity  # Then, to
                #  such specific key, sum the quantity being added from the
                #  request to the one available via the specified key/size
                messages.success(request, f"Updated "
                                          f"{''.join(list(size)[0:1])}."
                                          f"{''.join(list(size)[-3:])} "
                                          f"{product.name} in your bag")
            else:
                """
                    If there is no key/size in the dictionary of such item_id
                """
                bag[item_id]['items_by_size'][size] = quantity  # Then,
                #  set the new quantity for such key/size
                messages.success(request, f"Added "
                                          f"{''.join(list(size)[0:1])}."
                                          f"{''.join(list(size)[-3:])} "
                                          f"{product.name} to your bag")
        else:
            """
                If the item id was not previously added to the bag session data
            """
            bag[item_id] = {'items_by_size': {size: quantity}}  # Then, create
            # it
            messages.success(request, f"Added "
                                      f"{''.join(list(size)[0:1])}."
                                      f"{''.join(list(size)[-3:])} "
                                      f"{product.name} to your bag")
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity in '
                                      f'your bag')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def update_bag(request, item_id):
    """ Update the quantity of the specified product via the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None

    if 'product_size' in request.POST:
        """product_size passed via the related input and name attribute"""
        size = request.POST['product_size']  # Then, assign it
    bag = request.session.get('bag', {})  # Now, update the bag session data

    if size:
        """if size has been honoured through the logic above"""
        # Uncomment the following if st, when 0 quantity allowed via js
        # if quantity > 0:
        bag[item_id]['items_by_size'][size] = quantity
        # else:
        #     del bag[item_id]['items_by_size'][size]
        #     if not bag[item_id]['items_by_size']:
        #         bag.pop(item_id)
        messages.success(request, f"Quantity of "
                                  f"{''.join(list(size)[0:1])}."
                                  f"{''.join(list(size)[-3:])} {product.name}"
                                  f" successfully updated.")
    else:
        # Uncomment the following if st, when 0 quantity allowed via js
        # if quantity > 0:
        bag[item_id] = quantity
        # else:
        #     bag.pop(item_id)
        messages.success(request, f"Quantity of {product.name}"
                                  f" successfully updated.")

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove item entirely from the shoping bag"""

    product = get_object_or_404(Product, pk=item_id)
    try:
        size = None
        if 'size' in request.POST:
            """product_size passed via the related input and name attribute"""
            size = request.POST['size']  # Then, assign it
        bag = request.session.get('bag', {})  # Now, update the bag
        # session data

        if size:
            """if size has been honoured through the logic above"""
            if not bag[item_id]['items_by_size']:
                """If there is only one size in regard to a product"""
                bag.pop(item_id)
                messages.success(request, f"{''.join(list(size)[0:1])}."
                                          f"{''.join(list(size)[-3:])} "
                                          f"{product.name} successfully"
                                          f" removed from your bag")
            else:
                """If there are multiple sizes in regard to a product"""
                del bag[item_id]['items_by_size'][size]
                messages.success(request, f"{''.join(list(size)[0:1])}."
                                          f"{''.join(list(size)[-3:])} "
                                          f"{product.name} successfully"
                                          f" removed from your bag")
        else:
            bag.pop(item_id)
            messages.success(request, f'{product.name} successfully removed'
                                      f'from your bag')

        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)

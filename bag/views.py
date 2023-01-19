from django.shortcuts import render, redirect


def view_bag(request):
    """ A view to return the bag page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

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
                bag[item_id]['items_by_size'][size] += quantity # Then, to such
                #  specific key, sum the quantity being added from the request
                # to the one available via the specified key/size
            else:
                """
                    If there is no key/size in the dictionary of such item_id
                """
                bag[item_id]['items_by_size'][size] = quantity  # Then,
                #  set the new quantity for such key/size
        else:
            """
                If the item id was not previously added to the bag session data
            """
            bag[item_id] = {'items_by_size': {size: quantity}}  # Then, create
            # it
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)

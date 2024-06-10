from django.shortcuts import render, redirect
from .models import PurchaseOrderItem
from .forms import PurchaseOrderForm



# Create your views here.
def create_purchase_order(request):

    print("This api has been called")  # Add this print statement

    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            # Create a new purchase order instance
            purchase_order = form.save(commit=False)
            purchase_order.status = 'draft'  # Set initial status
            purchase_order.save()

            # Loop through form data to create purchase order items
            for item_data in form.cleaned_data['items']:
                item = item_data['item']
                quantity = item_data['quantity']
                price = item_data['price']

                # Create a new purchase order item instance
                purchase_order_item = PurchaseOrderItem.objects.create(
                    purchase_order=purchase_order,
                    item=item,
                    quantity=quantity,
                    price=price
                )

                # Update inventory quantities
                item.quantity += quantity
                item.save()

            return redirect('purchase_order_detail', pk=purchase_order.pk)
    else:
        form = PurchaseOrderForm()
    
    return render(request, 'create_purchase_order.html', {'form': form})
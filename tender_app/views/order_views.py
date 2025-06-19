"""
Order and shop-related views for the tender application.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from ..models import BreakfastItem, Order, OrderItem
from .tender_views import has_user_role


@login_required
@user_passes_test(has_user_role)
def shop_view(request):
    """View to display available breakfast items in the shop."""
    breakfast_items = BreakfastItem.objects.filter(available=True)
    return render(request, 'shop.html', {'breakfast_items': breakfast_items})


@login_required
@user_passes_test(has_user_role)
def order_list_view(request):
    """View to list all orders for the current user."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_list.html', {'orders': orders})


@login_required
@user_passes_test(has_user_role)
def add_to_order_view(request, item_id):
    """View to add an item to the user's current order."""
    if request.method == 'POST':
        item = get_object_or_404(BreakfastItem, id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        
        # Get or create pending order
        order, created = Order.objects.get_or_create(
            user=request.user,
            status='pending'
        )
        
        # Add item to order
        OrderItem.objects.create(
            order=order,
            item=item,
            quantity=quantity,
            price=item.price
        )
        
        # Update total amount
        order.total_amount = sum(
            item.price * item.quantity 
            for item in order.orderitem_set.all()
        )
        order.save()
        
        messages.success(request, f'{quantity}x {item.name} added to your order!')
        
    return redirect('shop')

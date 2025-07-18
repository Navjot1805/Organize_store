
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Item
from .forms import ItemForm

@login_required
def item_list(request):
    items = Item.objects.filter(created_by=request.user)
    total_value = sum(item.quantity * item.price for item in items)
    total_items = items.count()
    low_stock = items.filter(quantity__lte=5)
    return render(request, 'inventory/item_list.html', {
        'items': items,
        'total_value': total_value,
        'total_items': total_items,
        'low_stock': low_stock,
    })

@login_required
def item_add(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            messages.success(request, "Item added successfully!")
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'inventory/item_form.html', {'form': form})

@login_required
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated.")
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'inventory/item_form.html', {'form': form})

@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Item deleted.")
        return redirect('item_list')
    return render(request, 'inventory/item_confirm_delete.html', {'item': item})

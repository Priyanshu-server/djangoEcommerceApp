from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import View, TemplateView, CreateView, DeleteView, UpdateView, ListView, DetailView
from .models import Item, OrderItem, Order
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home-page.html"


class ProductDetailView(DetailView):
    model = Item
    template_name = "product-page.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, is_ordered=False)
            context = {
                'object': order
            }
            return render(self.request, "order-summary.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have any active order!")
            return redirect("/")


def checkout(request):
    context = {
        'Item': Item.objects.all()
    }
    return render(request, "checkout-page.html", context)


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, is_ordered=False)

    order_qs = Order.objects.filter(user=request.user, is_ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated in your Cart !")
        else:
            messages.info(request, "This item was added to your Cart !")
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)

        messages.info(request, "This item quantity was updated in your Cart !")

    return redirect("home:order-summary")


# Removing from the Cart
@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    order_qs = Order.objects.filter(user=request.user, is_ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                is_ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart !")
        else:
            messages.info(request, "This item was not in your cart !")
            return redirect("home:order-summary")
    else:
        # add a message that user doesn't have an order
        messages.info(request, "You don't have any order right now !")
        return redirect("home:order-summary")
    return redirect("home:order-summary")


# Removing from the Cart
@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    order_qs = Order.objects.filter(user=request.user, is_ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                is_ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated !")
        else:
            messages.info(request, "This item was not in your cart !")
            return redirect("home:order-summary")
    else:
        # add a message that user doesn't have an order
        messages.info(request, "You don't have any order right now !")
        return redirect("home:product", slug=slug)

    return redirect("home:order-summary")

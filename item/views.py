import stripe
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import TemplateView

from item.models import Item
from TestRishatProject import settings


stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(View):
    """Представление для создании сессии покупки"""
    def get(self, request, *args, **kwargs):
        item_id = self.kwargs['pk']
        item = Item.objects.get(id=item_id)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': item.price,
                        'product_data': {
                            'name': item.name
                        },
                    },
                    'quantity': 1,
                },
            ],
            metadata={
                'item_id': item.id
            },
            mode='payment',
            success_url='http://127.0.0.1:8000' + '/success/',
            cancel_url='http://127.0.0.1:8000' + '/cancel/',
        )
        return JsonResponse({
            'id': checkout_session.id
        })


class SuccessView(TemplateView):
    """Представление для успешной покупки"""
    template_name = "success.html"


class CancelView(TemplateView):
    """Представление для отмены"""
    template_name = "cancel.html"


class ProductLandingPageView(TemplateView):
    """Представление для товара"""
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        item = Item.objects.get(id=kwargs['pk'])
        context = super(ProductLandingPageView, self).\
            get_context_data(**kwargs)
        context.update({
            "item": item,
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
        })
        return context

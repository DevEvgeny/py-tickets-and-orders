from typing import List, Dict

from django.db import transaction

from django.contrib.auth import get_user_model

from db.models import Order, Ticket, MovieSession, User


def create_order(
        tickets: List[Dict[str, int]],
        username: str,
        date: str = None
) -> Order | None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = user.objects.create(user=user)

        if date:
            order.created_at = date
        order.save()

        for ticket_data in tickets:
            Ticket.objects.create(
                movie_session_id=ticket_data["movie_session"],
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )
        return order

def get_orders(username: str = None) -> Order:
    if username:
        return list(Order.objects.filter(user__username=username))
    return list(Order.objects.all())

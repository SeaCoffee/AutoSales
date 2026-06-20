from django.db import models


class ListingQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def inactive(self):
        return self.filter(active=False)

    def for_seller(self, seller):
        return self.filter(seller=seller)

    def with_related(self):
        return self.select_related(
            'car',
            'car__brand',
            'car__model_name',
            'seller',
            'currency',
        )


class ListingManager(models.Manager.from_queryset(ListingQuerySet)):
    pass
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

from clients.models import Company, Branch

class User(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_accounter = models.BooleanField(default=False)
    is_salesman = models.BooleanField(default=False)
    is_delivery_person = models.BooleanField(default=False)

    is_client = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        if self.is_staff:
            if self.is_client or self.company or self.branch:
                raise ValidationError("Packford employee not authorized to work at other Company")

        if self.is_client:
            if self.is_manager or self.is_accounter or self.is_salesman or self.is_delivery_person:
                raise ValidationError("Client staff not authorized to grant these selected permissions (manager, accounter, salesman, delivery person)")
            if not self.company and not self.branch:
                raise ValidationError("The employee must belong to a either company or branch")
    

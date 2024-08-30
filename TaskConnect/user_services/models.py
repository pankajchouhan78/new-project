from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from user_services.manager import TaskManager
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



class Address(models.Model):
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=8)
    country = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"{self.street} - {self.city}"

class Role(models.Model):
    role_name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.role_name
    
class Organization(models.Model):
    name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    contact_email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    

class BaseModel(models.Model):
    name = models.CharField(max_length=25)
    # Field-Level Validation
    phone = models.CharField(
        max_length=12,
        unique=True,
        validators=[
            MinLengthValidator(10),  # Ensures the phone number has at least 10 characters
            RegexValidator(regex=r'^\d{10,12}$', message="Phone number must be 10-12 digits long.")
        ],
        blank=True,null=True
    )
    gender = models.CharField(max_length=1, choices=(
        ('M', 'Male'),
        ('F', 'Female'),
    ),null=True, blank=True)
    profile_pic = models.ImageField(upload_to="profile/", blank=True, null=True)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True, blank=True)  # Used SET_NULL instead of CASCADE
    location = models.CharField(max_length=100, blank=True, null=True)  # Combined latitude and longitude
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class User(BaseModel, AbstractBaseUser):
    USER_TYPE_CHOICES = [
        ('Customer', 'Customer'),
        ('ServiceProvider', 'ServiceProvider'),
    ]

    WORK_CHOICES = [
        ('REQUESTED', 'Requested'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    email = models.EmailField(
        max_length=30,
        unique=True,
        validators=[
            RegexValidator(regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', message="Enter a valid email address.")
        ]
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='Customer')
    work_status = models.CharField(max_length=20, choices=WORK_CHOICES, null=True, blank=True)
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True)
    user_role = models.ManyToManyField('Role', related_name="user_profiles", blank=True, null=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = TaskManager()
    #  Model-Level Validation:
    def clean(self):
        # Restrict Customer from having any roles
        if self.user_type == 'Customer' and (self.user_role != "" or self.user_role not in None):
            raise ValidationError("Customers cannot be assigned any roles.")
        
        # if self.user_type == 'Customer' and self.organization.exists():
        #     raise ValidationError("Customers cannot be assigned any organization.")

        # if self.gender not in ['M', 'F']:
        #     raise ValidationError("Gender must be 'M' (Male) or 'F' (Female).")

        # if len(self.phone) != 10:
        #     raise ValidationError("Phone number must be exactly 10 digits long.")

    def save(self, *args, **kwargs):
        # Always call the full_clean() method before saving
        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Feedback(models.Model):
    from_user = models.ForeignKey(User, related_name='feedback_given', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='feedback_received', on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=1, choices=[(i, str(i)) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback from {self.from_user.name} to {self.to_user.name}'  


# Custom Validators

def validate_price(value):
    if value < 0:
        raise ValidationError(
            _('%(value)s is not an Positive number'),
            params={'value': value},
        )

class Service(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)  # e.g., Plumber, Electrician
    service_name = models.CharField(max_length=100)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_price])  # Base service charge

    def __str__(self):
        return f'{self.service_name} ({self.role.role_name})'


class Component(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='components', null=True, blank=True)
    component_name = models.CharField(max_length=100)
    component_price = models.DecimalField(max_digits=10, decimal_places=2)  # Price for the component

    def __str__(self):
        return f'{self.component_name} for {self.service.service_name if self.service else "Unknown Service"}'


class Bill(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    components = models.ManyToManyField(Component, blank=True)  # Optional, can be empty
    service_charge = models.DecimalField(max_digits=10, decimal_places=2)
    total_component_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Tax rate as a percentage
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Paid', 'Paid')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total_component_charge(self):
        total = sum(component.component_price for component in self.components.all())
        self.total_component_charge = total
        return total

    def calculate_total_amount(self):
        subtotal = self.service_charge + self.total_component_charge - self.discount
        tax_amount = subtotal * (self.tax_rate / 100)
        self.total_amount = subtotal + tax_amount
        return self.total_amount

    def mark_as_paid(self):
        self.payment_status = 'Paid'
        self.save()

    def save(self, *args, **kwargs):
        self.calculate_total_component_charge()  # Calculate component charges
        self.calculate_total_amount()  # Calculate the final bill
        super(Bill, self).save(*args, **kwargs)

    def __str__(self):
        return f'Bill for {self.service.service_name} on {self.created_at}'


class Payment(models.Model):

    PAYMENT_METHOD = [
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('PayPal', 'PayPal'),
        ('Cash', 'Cash')
        ]
    PAYMENT_STATUS = [('Pending', 'Pending'), ('Completed', 'Completed')]
    
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, choices= PAYMENT_STATUS,default='Pending')

    def complete_payment(self):
        self.payment_status = 'Completed'
        self.save()
        # Mark the bill as paid once payment is completed
        self.bill.mark_as_paid()

    def __str__(self):
        return f'Payment of {self.payment_amount} for {self.bill}'






    
# class User(AbstractBaseUser):

#     GENDER_CHOICES = (
#         ('M', 'Male'),
#         ('F', 'Female'),
#     )

#     USER_TYPE_CHOICES = [
#         ('Customer', 'Customer'),
#         ('ServiceProvider', 'ServiceProvider'),
#     ]

#     work_status = [
#         ('REQUESTED', 'Requested'),
#         ('IN_PROGRESS', 'In Progress'),
#         ('COMPLETED', 'Completed'),
#         ('CANCELLED', 'Cancelled'),
#     ]

#     name = models.CharField(max_length=25)
#     email = models.EmailField(max_length=30, unique=True)
#     phone = models.CharField(max_length=12, unique=True)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
#     user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='Customer')

#     work_status = models.CharField(
#         max_length=20,
#         choices=[
#             ('requested', 'Requested'),
#             ('in_progress', 'In Progress'),
#             ('completed', 'Completed'),
#             ('canceled', 'Canceled'),
#         ],
#         default='requested'
#     )

#     profile_pic = models.ImageField(upload_to="profile/", blank=True, null=True)
#     address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)  # Used SET_NULL instead of CASCADE
#     location = models.CharField(max_length=100, blank=True, null=True)  # Combined latitude and longitude

#     organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
#     user_role = models.ManyToManyField(Role, blank=True, null=True, related_name="user_profiles")
    

#     date_joined = models.DateTimeField(auto_now_add=True)
#     last_login = models.DateTimeField(auto_now=True)

#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=False)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["name"]

#     objects = TaskManager()

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return self.is_admin

#     def has_module_perms(self, app_label):
#         return True



# class PaymentMethod(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
#     card_number = models.CharField(max_length=16)
#     cardholder_name = models.CharField(max_length=100)
#     expiry_date = models.CharField(max_length=5)  # Format: MM/YY
#     cvv = models.CharField(max_length=3)

#     def __str__(self):
#         return f"{self.cardholder_name} - {self.card_number[-4:]}"

# class Invoice(models.Model):
#     organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='invoices', null=True, blank=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     issued_date = models.DateTimeField(auto_now_add=True)
#     due_date = models.DateTimeField()
#     is_paid = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Invoice {self.id} - {self.amount} for {self.user.name}"

# class Payment(models.Model):
#     invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
#     payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     paid_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, choices=[('Success', 'Success'), ('Failed', 'Failed')])

#     def __str__(self):
#         return f"Payment {self.id} - {self.amount} via {self.payment_method}"

# class Transaction(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
#     payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
#     transaction_date = models.DateTimeField(auto_now_add=True)
#     transaction_type = models.CharField(max_length=20, choices=[('Debit', 'Debit'), ('Credit', 'Credit')])
#     description = models.TextField()

#     def __str__(self):
#         return f"Transaction {self.id} - {self.transaction_type} for {self.user.name}"
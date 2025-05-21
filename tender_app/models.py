from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from django.core.validators import FileExtensionValidator
from django.db import migrations



class TenderTracker(models.Model):
    year = models.IntegerField(unique=True)  # Ensures one entry per year
    last_sequence = models.IntegerField(default=0)  # sequence counter

    def __str__(self):
        return f"{self.year} - {self.last_sequence}"

    @classmethod
    def get_next_sequence(cls, year):
        tracker, created = cls.objects.get_or_create(year=year)
        tracker.last_sequence += 1
        tracker.save()
        return tracker.last_sequence


class Department(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Tender(models.Model):
    CATEGORY_CHOICES = [
        ('Goods', 'Goods'),
        ('Technical Service', 'Technical Service'),
        ('Consultancy', 'Consultancy'),
        ('Works', 'Works'),
    ]
    
    STATUS_CHOICES = [
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    CURRENCY_CHOICES = [
        ('GHS', 'GHS'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    ]

    # Existing fields
    tender_number = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # New fields
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Progress')
    requests_aggregated = models.IntegerField(default=0)
    invitation_date = models.DateField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True)
    evaluation_date = models.DateField(null=True, blank=True)
    contract_date = models.DateField(null=True, blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='GHS')
    contract_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    vendor_name = models.CharField(max_length=200, blank=True)
    po_date = models.DateField(null=True, blank=True)
    po_number = models.CharField(max_length=100, blank=True)
    sra_date = models.DateField(null=True, blank=True)
    sra_number = models.CharField(max_length=100, blank=True)
    payment_memo_date = models.DateField(null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    file_name = models.CharField(max_length=200, blank=True)
    file_number = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-created_at']

    def get_officer_name(self):
        return self.user.profile.full_name

    def __str__(self):
        return f"{self.tender_number} - {self.get_officer_name()}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name


class Category(models.Model):
    code = models.CharField(max_length=10, unique=True)  # e.g., A.4.1
    name = models.CharField(max_length=255)  # e.g., Category Name

    def __str__(self):
        return f"{self.code} - {self.name}"


class BreakfastItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(
        upload_to='breakfast_items/',
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']),
        ],
        help_text="Upload an image (JPG, PNG or WebP, max 5MB)"
    )
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - GHS {self.price}"

    def clean(self):
        if self.image and self.image.size > 5 * 1024 * 1024:  # 5MB
            raise ValidationError('Image file too large ( > 5MB )')


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(BreakfastItem, through='OrderItem')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.get_full_name()}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(BreakfastItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.item.name}"


class Division(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"


class ISOTracker(models.Model):
    year = models.IntegerField(unique=True)
    last_sequence = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.year} - {self.last_sequence}"

    @classmethod
    def get_next_sequence(cls, year):
        tracker, created = cls.objects.get_or_create(year=year)
        tracker.last_sequence += 1
        tracker.save()
        return tracker.last_sequence


class ISONumber(models.Model):
    LETTER_TYPES = [
        ('RFQ', 'RFQ Letter'),
        ('PPA', 'Letter to PPA'),
        ('CTR', 'Letter to CTRC'),
    ]
    
    iso_number = models.CharField(max_length=50, unique=True)
    date_created = models.DateField(auto_now_add=True)
    officer = models.ForeignKey(User, on_delete=models.CASCADE)
    tender = models.ForeignKey('Tender', on_delete=models.CASCADE)
    division = models.ForeignKey('Division', on_delete=models.CASCADE)  # Keep this as is
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    letter_type = models.CharField(max_length=3, choices=LETTER_TYPES)
    description = models.TextField()

    def __str__(self):
        return self.iso_number


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_person = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class FrameworkAgreement(models.Model):
    tender = models.ForeignKey('Tender', on_delete=models.CASCADE, related_name='framework_agreements')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='framework_agreements')
    start_date = models.DateField()
    end_date = models.DateField()
    agreement_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, choices=[
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('terminated', 'Terminated')
    ])
    terms_conditions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.agreement_number} - {self.vendor.name}"

    class Meta:
        ordering = ['-created_at']


class TenderItem(models.Model):
    tender = models.ForeignKey('Tender', on_delete=models.CASCADE, related_name='items')
    item_name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_of_measure = models.CharField(max_length=50)
    
    # Chemical-specific fields
    chemical_grade = models.CharField(max_length=255, blank=True, null=True, help_text="e.g., HPLC Grade, Analytical Reagent Grade")
    molar_mass = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 88.11 g/mol")
    chemical_formula = models.CharField(max_length=255, blank=True, null=True, help_text="e.g., CH3COCH3")
    density = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., 0.791 g/mL at 25°C")
    vapor_density = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., 2 (vs air)")
    assay_percentage = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., ≥99.8%")
    physical_form = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Solvent, Powder, Crystal")
    package_size = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 2.5L, 500ml")
    appearance = models.CharField(max_length=255, blank=True, null=True, help_text="e.g., Colorless liquid")
    impurities = models.TextField(blank=True, null=True, help_text="List of impurity limits")
    specifications = models.TextField(blank=True, null=True)
    
    # Existing fields
    brand = models.CharField(max_length=255, blank=True, null=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    specifications = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item_name} - {self.tender.tender_number}"

    class Meta:
        ordering = ['item_name']


class VendorBid(models.Model):
    tender = models.ForeignKey('Tender', on_delete=models.CASCADE, related_name='bids')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    tender_item = models.ForeignKey(TenderItem, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=15, decimal_places=2)
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3, default='GHS')  # ISO currency code
    is_winner = models.BooleanField(default=False)
    technical_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    financial_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    total_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto-calculate total price if unit price and quantity change
        self.total_price = self.unit_price * self.tender_item.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.vendor.name} - {self.tender_item.item_name}"

    class Meta:
        ordering = ['-total_score', 'total_price']
        unique_together = ['tender', 'vendor', 'tender_item']


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(
            user=instance,
            full_name=f"{instance.first_name} {instance.last_name}".strip() or instance.username
        )

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        UserProfile.objects.create(
            user=instance,
            full_name=f"{instance.first_name} {instance.last_name}".strip() or instance.username
        )
    else:
        instance.profile.save()

def create_divisions(apps, schema_editor):
    Division = apps.get_model('tender_app', 'Division')
    divisions = [
        ('HR', 'HR Division'),
        ('ITMS', 'ITMS Division'),
        ('FIN', 'Finance Division'),
        ('CLSR', 'Centre for Laboratory Services and Research'),
        ('HPTD', 'Health Products and Technologies Division'),
        ('QMSD', 'Quality Assurance Division'),
        ('CSD', 'Corporate Services Division'),
        ('FD', 'Food Division'),
    ]
    for code, name in divisions:
        Division.objects.create(code=code, name=name)

class Migration(migrations.Migration):
    dependencies = [
        ('tender_app', 'previous_migration'),  # Replace with your last migration
    ]

    operations = [
        migrations.RunPython(create_divisions),
    ]

class Chemical(models.Model):
    CHEMICAL_GRADES = [
        ('HPLC', 'High Performance Liquid Chromatography Grade'),
        ('AR', 'Analytical Reagent Grade'),
        ('GC', 'Gas Chromatography Grade'),
        ('USP', 'United States Pharmacopeia Grade'),
        ('ACS', 'American Chemical Society Grade'),
        ('TECH', 'Technical Grade'),
        ('GEN', 'General Purpose Reagent Grade'),
    ]

    lot_number = models.CharField(max_length=10)
    chemical_name = models.CharField(max_length=255)
    formula = models.CharField(max_length=100, blank=True)
    grade = models.CharField(max_length=10, choices=CHEMICAL_GRADES)
    package_size = models.CharField(max_length=50)
    quantity = models.IntegerField()
    tender_item = models.ForeignKey('TenderItem', on_delete=models.CASCADE, related_name='chemicals')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.chemical_name} ({self.lot_number})"

    class Meta:
        ordering = ['chemical_name', 'lot_number']


class ChemicalSpecification(models.Model):
    SPEC_TYPES = [
        ('MOLAR_MASS', 'Molar Mass'),
        ('DENSITY', 'Density'),
        ('ASSAY', 'Assay'),
        ('PURITY', 'Purity'),
        ('APPEARANCE', 'Appearance'),
        ('VAPOR_DENSITY', 'Vapor Density'),
        ('IMPURITY', 'Impurity Limit'),
        ('PH', 'pH'),
        ('BOILING_POINT', 'Boiling Point'),
        ('FLASH_POINT', 'Flash Point'),
        ('SOLUBILITY', 'Solubility'),
        ('OTHER', 'Other'),
    ]

    chemical = models.ForeignKey(Chemical, on_delete=models.CASCADE, related_name='specifications')
    spec_type = models.CharField(max_length=20, choices=SPEC_TYPES)
    value = models.CharField(max_length=255)
    unit = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.chemical.chemical_name} - {self.get_spec_type_display()}: {self.value} {self.unit}"

    class Meta:
        ordering = ['chemical', 'spec_type']
        unique_together = ['chemical', 'spec_type']


from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User

from decimal import Decimal, ROUND_HALF_UP
from products.models import (
    Product,
    Category,
    SubCategory,
    Brand,
    Thickness,
    Colour,
    Design,
)


# ==========================================================
# ORDER
# ==========================================================

class Order(models.Model):

    # ======================================================
    # STATUS
    # ======================================================

    STATUS_CHOICES = [
        ("Pending 1", "Pending 1"),
        ("Pending 2", "Pending 2"),
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
        ("Out of Stock", "Out of Stock"),
    ]


    # ======================================================
    # LOADING LOCATION
    # ======================================================

    LOADING_CHOICES = [
        ("G-1", "G-1"),
        ("WS", "WS"),
        ("PVR", "PVR"),
        ("G-2", "G-2"),
    ]


    # ======================================================
    # DISPATCH STATUS
    # ======================================================

    DISPATCH_STATUS_CHOICES = [
        ("Not Dispatched", "Not Dispatched"),
        ("Dispatched", "Dispatched"),
    ]


    # ======================================================
    # LOCATION
    # ======================================================

    LOCATION_CHOICES = [
        ("ERNAKULAM-GOSHREE ROUTE", "ERNAKULAM-GOSHREE ROUTE"),
        ("ERNAKULAM-EDAPPALLY-ROUTE", "ERNAKULAM-EDAPPALLY-ROUTE"),
        ("PALAKKAD-ROUTE", "PALAKKAD-ROUTE"),
        ("WAYANAD-ROUTE", "WAYANAD-ROUTE"),
        ("CALICUT-ROUTE", "CALICUT-ROUTE"),
        ("NILABUR-MANCHERY-ROUTE", "NILABUR-MANCHERY-ROUTE"),
        ("NILABUR-PERINTHALMANNA-ROUTE", "NILABUR-PERINTHALMANNA-ROUTE"),
    ]


    # ======================================================
    # SALES MEMBER
    # ======================================================

    sales_member = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sales_orders",
    )


    # ======================================================
    # CUSTOMER DETAILS
    # ======================================================

    customer_name = models.CharField(
        max_length=150,
    )

    phone = models.CharField(
        max_length=10,
        blank=True,
    )

    company_name = models.CharField(
        max_length=150,
        blank=True,
    )

    location = models.CharField(
        max_length=50,
        choices=LOCATION_CHOICES,
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )


    # ======================================================
    # PRODUCT
    # ======================================================

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )


    # ======================================================
    # CATEGORY
    # ======================================================

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="orders",
        null=True,
        blank=True,
    )


    # ======================================================
    # SUB CATEGORY
    # ======================================================

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )

    subcategory_text = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    

    

    # ======================================================
    # BRAND
    # ======================================================

    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )


    # ======================================================
    # THICKNESS
    # ======================================================

    thickness = models.ForeignKey(
        Thickness,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )


    # ======================================================
    # COLOUR
    # ======================================================

    colour = models.ForeignKey(
        Colour,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )

    colour_text = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )


    # ======================================================
    # DESIGN
    # ======================================================

    design = models.ForeignKey(
        Design,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )

    design_text = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )


    # ======================================================
    # CATEGORY 2 - CORE NUMBER
    # ======================================================

    core_number = models.CharField(
        max_length=100,
        blank=True,
    )


    # ======================================================
    # CATEGORY 4 - SIZE
    # ======================================================

    size_text = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    
    # ======================================================
    # WIDTH - FEET
    # ======================================================

    width_ft = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )


    # ======================================================
    # WIDTH - METERS
    # ======================================================

    width_meter = models.DecimalField(
        max_digits=10,
        decimal_places=4,
        null=True,
        blank=True,
    )


    # ======================================================
    # LENGTH - FEET
    # ======================================================

    length_ft = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )


    # ======================================================
    # CATEGORY 3 - NUMBER OF PRODUCTS
    # ======================================================

    sheets = models.PositiveIntegerField(
        default=0,
    )


    # ======================================================
    # SQUARE METER
    # ======================================================

    sq_mtr = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )


    # ======================================================
    # SQM PRICE
    # ======================================================

    sqm_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        null=True,
        blank=True,
    )


    # ======================================================
    # RATE
    # ======================================================

    rate = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )


    # ======================================================
    # AMOUNT
    # ======================================================

    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0,
    )


    # ======================================================
    # LOADING FROM
    # ======================================================

    loading_from = models.CharField(
        max_length=50,
        choices=LOADING_CHOICES,
        blank=True,
    )


    # ======================================================
    # ORDER TAKEN BY
    # ======================================================

    order_taken_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="taken_orders",
    )


    # ======================================================
    # REMARKS
    # ======================================================

    remarks = models.TextField(
        blank=True,
        null=True,
    )


    # ======================================================
    # STATUS
    # ======================================================

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending1",
    )


    # ======================================================
    # DISPATCH
    # ======================================================

    dispatch_status = models.CharField(
        max_length=20,
        choices=DISPATCH_STATUS_CHOICES,
        default="Not Dispatched",
    )

    dispatch_date = models.DateField(
        null=True,
        blank=True,
    )

    dispatched_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dispatched_orders",
    )


    # ======================================================
    # CREATED DATE
    # ======================================================

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


    # ======================================================
    # UPDATED DATE
    # ======================================================

    updated_at = models.DateTimeField(
        auto_now=True,
    )


    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"

    # ======================================================
# SAVE
# ======================================================

def save(self, *args, **kwargs):

    # ==================================================
    # PRODUCT → AUTOMATIC DETAILS
    # ==================================================

    if self.product:

        product = self.product

        # CATEGORY
        self.category = product.category

        # SUB CATEGORY
        self.subcategory = product.subcategory

        if product.subcategory:
            self.subcategory_text = product.subcategory.name
        else:
            self.subcategory_text = ""

        # BRAND
        self.brand = product.brand

        # THICKNESS
        self.thickness = product.thickness

        # COLOUR
        self.colour = product.colour

        if product.colour:
            self.colour_text = product.colour.name
        else:
            self.colour_text = ""

        # DESIGN
        self.design = product.design

        if product.design:
            self.design_text = product.design.name
        else:
            self.design_text = ""

        # WIDTH
        if product.width_ft is not None:
            self.width_ft = product.width_ft

        # CORE NUMBER
        if product.core_number:
            self.core_number = product.core_number

        # CATEGORY 4 SIZE
        if product.size:
            self.size_text = product.size

        # PRODUCT RATE
        if product.sqt_rate is not None:
            self.rate = product.sqt_rate


    # ==================================================
    # WIDTH FEET → WIDTH METER
    # ==================================================

    if self.width_ft is not None:

        self.width_meter = (
            Decimal(str(self.width_ft))
            * Decimal("0.3048")
        ).quantize(
            Decimal("0.0001"),
            rounding=ROUND_HALF_UP
        )

    else:

        self.width_meter = None


    # ==================================================
    # CATEGORY NAME
    # ==================================================

    category_name = ""

    if self.category and self.category.name:

        category_name = (
            self.category.name
            .strip()
            .lower()
            .replace(" ", "")
            .replace("-", "")
            .replace("_", "")
        )


    # ==================================================
    # CATEGORY 1
    # LENGTH × RATE
    # ==================================================

    if category_name == "category1":

        self.amount = (
            Decimal(str(self.length_ft or 0))
            * Decimal(str(self.rate or 0))
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )


    # ==================================================
    # CATEGORY 2
    # LENGTH × RATE
    # ==================================================

    elif category_name == "category2":

        self.amount = (
            Decimal(str(self.length_ft or 0))
            * Decimal(str(self.rate or 0))
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )


    # ==================================================
    # CATEGORY 3
    # NUMBER OF PRODUCTS × RATE
    # ==================================================

    elif category_name == "category3":

        self.amount = (
            Decimal(str(self.sheets or 0))
            * Decimal(str(self.rate or 0))
        ).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )


    # ==================================================
    # CATEGORY 4
    # ==================================================

    elif category_name == "category4":

        if self.amount is None:

            self.amount = Decimal("0.00")


    # ==================================================
    # DEFAULT
    # ==================================================

    else:

        if self.amount is None:

            self.amount = Decimal("0.00")


    # ==================================================
    # SAVE
    # ==================================================

    super().save(*args, **kwargs)


# ======================================================
# STRING
# ======================================================

def __str__(self):

    product_name = (
        self.product.product_name
        if self.product
        else "No Product"
    )

    return (
        f"Order #{self.id} - "
        f"{self.customer_name} - "
        f"{product_name}"
    )
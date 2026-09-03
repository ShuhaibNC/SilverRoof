from django.db import models


# ==========================================================
# CATEGORY
# ==========================================================

class Category(models.Model):

    name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name


# ==========================================================
# SUB CATEGORY
# ==========================================================

class SubCategory(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories"
    )

    name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name


# ==========================================================
# BRAND
# ==========================================================

class Brand(models.Model):

    name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name


# ==========================================================
# THICKNESS
# ==========================================================

class Thickness(models.Model):

    name = models.CharField(
        max_length=50
    )

    def __str__(self):
        return self.name


# ==========================================================
# COLOUR
# ==========================================================

class Colour(models.Model):

    name = models.CharField(
        max_length=50
    )

    def __str__(self):
        return self.name


# ==========================================================
# DESIGN
# ==========================================================

class Design(models.Model):

    name = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.name


# ==========================================================
# PRODUCT
# ==========================================================

class Product(models.Model):

    # ------------------------------------------------------
    # CATEGORY
    # ------------------------------------------------------

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    # ------------------------------------------------------
    # PRODUCT NAME
    # ------------------------------------------------------

    product_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    # ------------------------------------------------------
    # SUB CATEGORY
    # ------------------------------------------------------

    subcategory = models.ForeignKey(
        SubCategory,
        on_delete=models.SET_NULL,
        related_name="products",
        blank=True,
        null=True
    )

    # ------------------------------------------------------
    # MANUALLY TYPED SUB CATEGORY
    # ------------------------------------------------------

    subcategory_text = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    width = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )


    # ------------------------------------------------------
    # BRAND
    # ------------------------------------------------------

    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        related_name="products",
        blank=True,
        null=True
    )

    # ------------------------------------------------------
    # THICKNESS
    # ------------------------------------------------------

    thickness = models.ForeignKey(
        Thickness,
        on_delete=models.SET_NULL,
        related_name="products",
        blank=True,
        null=True
    )

    # ------------------------------------------------------
    # COLOUR
    # ------------------------------------------------------

    colour = models.ForeignKey(
        Colour,
        on_delete=models.SET_NULL,
        related_name="products",
        blank=True,
        null=True
    )

    # ------------------------------------------------------
    # DESIGN
    # ------------------------------------------------------

    design = models.ForeignKey(
        Design,
        on_delete=models.SET_NULL,
        related_name="products",
        blank=True,
        null=True
    )

    # ======================================================
    # WIDTH
    # ======================================================

    width_ft = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        blank=True,
        null=True
    )

    # ======================================================
    # CATEGORY 2 - CORE NUMBER
    # ======================================================

    core_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # ======================================================
    # CATEGORY 4 - SQFT RATE
    # ======================================================

    sqt_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        blank=True,
        null=True
    )

    # ======================================================
    # CATEGORY 4 - SIZE
    # ======================================================

    size = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

   

    # ======================================================
    # STRING
    # ======================================================

    def __str__(self):

        if self.product_name:

            return (
                f"{self.product_name} - "
                f"{self.category.name}"
            )

        if self.subcategory:

            return (
                f"{self.subcategory.name} - "
                f"{self.category.name}"
            )

        return (
            f"Product - "
            f"{self.category.name}"
        )


# ==========================================================
# PRODUCT STOCK
# ==========================================================

class ProductStock(models.Model):

    # ------------------------------------------------------
    # PRODUCT
    # ------------------------------------------------------

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="stock_details"
    )

    # ======================================================
    # CATEGORY 1 & 2
    # LENGTH STOCK
    # ======================================================

    length_ft = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        blank=True,
        null=True
    )

    # ======================================================
    # CATEGORY 3
    # NUMBER OF PRODUCTS
    # ======================================================

    quantity = models.PositiveIntegerField(
        default=0
    )

    # ======================================================
    # OUT OF STOCK
    # ======================================================

    out_of_stock = models.BooleanField(
        default=False
    )

    # ======================================================
    # UPDATED DATE
    # ======================================================

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # ======================================================
    # CATEGORY NAME HELPER
    # ======================================================

    def get_category_name(self):

        if not self.product.category:
            return ""

        return (
            self.product.category.name
            .strip()
            .lower()
            .replace(" ", "")
            .replace("-", "")
            .replace("_", "")
        )

    # ======================================================
    # SAVE
    # ======================================================

    def save(
        self,
        *args,
        **kwargs
    ):

        category_name = self.get_category_name()

        # --------------------------------------------------
        # CATEGORY 1
        # --------------------------------------------------

        if category_name == "category1":

            if not self.length_ft or self.length_ft <= 0:

                self.length_ft = 0

                self.out_of_stock = True

            else:

                self.out_of_stock = False

        # --------------------------------------------------
        # CATEGORY 2
        # --------------------------------------------------

        elif category_name == "category2":

            if not self.length_ft or self.length_ft <= 0:

                self.length_ft = 0

                self.out_of_stock = True

            else:

                self.out_of_stock = False

        # --------------------------------------------------
        # CATEGORY 3
        # --------------------------------------------------

        elif category_name == "category3":

            if self.quantity <= 0:

                self.quantity = 0

                self.out_of_stock = True

            else:

                self.out_of_stock = False

        # --------------------------------------------------
        # CATEGORY 4
        # --------------------------------------------------

        elif category_name == "category4":

            # Category 4 does not use stock reduction.

            self.out_of_stock = False

        super().save(
            *args,
            **kwargs
        )

    # ======================================================
    # STRING
    # ======================================================

    def __str__(self):

        return (
            f"{self.product.product_name} - "
            f"{self.product.category.name}"
        )


# ==========================================================
# CUSTOMER
# ==========================================================

class Customer(models.Model):

    LOCATION_CHOICES = [

        ("Palakkad", "Palakkad"),

        ("Malappuram", "Malappuram"),

        ("Ernakulam", "Ernakulam"),

    ]

    # ------------------------------------------------------
    # CUSTOMER NAME
    # ------------------------------------------------------

    customer_name = models.CharField(
        max_length=150
    )

    # ------------------------------------------------------
    # ADDRESS
    # ------------------------------------------------------

    address = models.TextField(
        blank=True
    )

    # ------------------------------------------------------
    # PHONE
    # ------------------------------------------------------

    phone = models.CharField(
        max_length=15
    )

    # ------------------------------------------------------
    # GST
    # ------------------------------------------------------

    gst_number = models.CharField(
        max_length=30,
        blank=True,
        null=True
    )

    # ------------------------------------------------------
    # LOCATION
    # ------------------------------------------------------

    location = models.CharField(
        max_length=20,
        choices=LOCATION_CHOICES
    )

    # ------------------------------------------------------
    # STRING
    # ------------------------------------------------------

    def __str__(self):

        return self.customer_name
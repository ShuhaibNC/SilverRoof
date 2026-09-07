from django import forms

from .models import (
    Product,
    Category,
    SubCategory,
    Brand,
    Thickness,
    Colour,
    Design,
    ProductStock,
)


# ==========================================================
# PRODUCT STOCK FORM
# ==========================================================

class ProductStockForm(forms.ModelForm):

    category = forms.ChoiceField(
        required=True,
        choices=[],
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_stock_category",
            }
        )
    )

    subcategory = forms.ChoiceField(
        required=True,
        choices=[],
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_stock_subcategory",
            }
        )
    )

    thickness = forms.ChoiceField(
        required=False,
        choices=[],
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_stock_thickness",
            }
        )
    )

    colour = forms.ChoiceField(
        required=False,
        choices=[],
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_stock_colour",
            }
        )
    )

    design = forms.ChoiceField(
        required=False,
        choices=[],
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_stock_design",
            }
        )
    )

    brand = forms.ChoiceField(
        required=False,
        choices=[],
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_stock_brand",
            }
        )
    )

    width = forms.ChoiceField(
        required=True,
        choices=[],
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_stock_width",
            }
        )
    )

    class Meta:

        model = ProductStock

        fields = [
            "product",
            "length_ft",
            "quantity",
            "out_of_stock",
        ]

        widgets = {

            "product": forms.HiddenInput(),

            "length_ft": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "id_length_ft",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "Enter available length in feet",
                }
            ),

            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "id_quantity",
                    "min": "0",
                    "placeholder": "Enter available quantity",
                }
            ),

            "out_of_stock": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                    "id": "id_out_of_stock",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["product"].required = False

        # All categories
        categories = Category.objects.all().order_by("name")

        self.fields["category"].choices = [
            ("", "Select Category")
        ] + [
            (str(category.id), category.name)
            for category in categories
        ]

        # Empty dependent dropdowns
        self.fields["subcategory"].choices = [
            ("", "Select Sub Category")
        ]

        self.fields["thickness"].choices = [
            ("", "Select Thickness")
        ]

        self.fields["colour"].choices = [
            ("", "Select Colour")
        ]

        self.fields["design"].choices = [
            ("", "Select Design")
        ]

        self.fields["brand"].choices = [
            ("", "Select Brand")
        ]

        self.fields["width"].choices = [
            ("", "Select Width")
        ]


# ==========================================================
# PRODUCT FORM
# ADMIN ADD / EDIT PRODUCT
# ==========================================================

class ProductForm(forms.ModelForm):

    product_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Product Name",
            }
        )
    )

    subcategory_text = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Sub Category",
            }
        )
    )

    brand_text = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Brand",
            }
        )
    )

    thickness_text = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Thickness",
            }
        )
    )

    colour_text = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Colour",
            }
        )
    )

    design_text = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Design",
            }
        )
    )

    nos = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": "0",
                "placeholder": "Enter Number of Items (NOS)",
            }
        )
    )

    class Meta:

        model = Product

        fields = [
            "category",
            "product_name",
            "subcategory_text",
            "width_ft",
            "thickness_text",
            "design_text",
            "colour_text",
            "brand_text",
            "core_number",
            "sqt_rate",
            "size",
            "nos",
        ]

        widgets = {

            "category": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "id_category",
                }
            ),

            "width_ft": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "Width in Feet",
                }
            ),

            "core_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Core Number",
                }
            ),

            "sqt_rate": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "Enter SQFT Rate",
                }
            ),

            "size": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Size",
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["category"].required = True
        self.fields["product_name"].required = True
        self.fields["subcategory_text"].required = True

        # These are only required for categories 1, 2 and 4.
        # Category 3 skips them entirely — enforced in clean().
        self.fields["brand_text"].required = False
        self.fields["colour_text"].required = False
        self.fields["width_ft"].required = False

        self.fields["thickness_text"].required = False
        self.fields["design_text"].required = False
        self.fields["core_number"].required = False
        self.fields["sqt_rate"].required = False
        self.fields["size"].required = False
        self.fields["nos"].required = False

        # Edit product initial values

        if self.instance and self.instance.pk:

            if self.instance.product_name:
                self.fields["product_name"].initial = (
                    self.instance.product_name
                )

            if self.instance.subcategory:
                self.fields["subcategory_text"].initial = (
                    self.instance.subcategory.name
                )

            elif self.instance.subcategory_text:
                self.fields["subcategory_text"].initial = (
                    self.instance.subcategory_text
                )

            if self.instance.brand:
                self.fields["brand_text"].initial = (
                    self.instance.brand.name
                )

            if self.instance.thickness:
                self.fields["thickness_text"].initial = (
                    self.instance.thickness.name
                )

            if self.instance.colour:
                self.fields["colour_text"].initial = (
                    self.instance.colour.name
                )

            if self.instance.design:
                self.fields["design_text"].initial = (
                    self.instance.design.name
                )

    # ======================================================
    # VALIDATION
    # ======================================================

    def clean(self):

        cleaned_data = super().clean()

        category = cleaned_data.get("category")

        product_name = (
            cleaned_data.get("product_name") or ""
        ).strip()

        subcategory_name = (
            cleaned_data.get("subcategory_text") or ""
        ).strip()

        brand_name = (
            cleaned_data.get("brand_text") or ""
        ).strip()

        colour_name = (
            cleaned_data.get("colour_text") or ""
        ).strip()

        width = cleaned_data.get("width_ft")

        if not product_name:
            self.add_error(
                "product_name",
                "Please enter Product Name."
            )

        if not subcategory_name:
            self.add_error(
                "subcategory_text",
                "Please enter Sub Category."
            )

        category_name = ""

        if category:
            category_name = (
                category.name
                .strip()
                .lower()
                .replace(" ", "")
                .replace("-", "")
                .replace("_", "")
            )

        # --------------------------------------------------
        # CATEGORY 1, 2, 4 — standard fields required
        # --------------------------------------------------
        if category_name in ("category1", "category2", "category4"):

            if not brand_name:
                self.add_error(
                    "brand_text",
                    "Please enter Brand."
                )

            if not colour_name:
                self.add_error(
                    "colour_text",
                    "Please enter Colour."
                )

            if width is None or width <= 0:
                self.add_error(
                    "width_ft",
                    "Please enter a valid width."
                )

        # --------------------------------------------------
        # CATEGORY 3 — only Product Name, NOS, Thickness
        # --------------------------------------------------
        if category_name == "category3":

            nos = cleaned_data.get("nos")

            if nos is None or nos < 0:
                self.add_error(
                    "nos",
                    "Please enter Number of Items (NOS)."
                )

        # Category 2 — Core Number is now optional
        # (kept on the model, no longer required in the form)

        # Category 4
        if category_name == "category4":

            sqt_rate = cleaned_data.get("sqt_rate")

            size = (
                cleaned_data.get("size") or ""
            ).strip()

            if sqt_rate is None:
                self.add_error(
                    "sqt_rate",
                    "Please enter SQFT Rate for Category 4."
                )

            elif sqt_rate < 0:
                self.add_error(
                    "sqt_rate",
                    "SQFT Rate cannot be negative."
                )

            if not size:
                self.add_error(
                    "size",
                    "Please enter Size for Category 4."
                )

        return cleaned_data


    # ======================================================
    # SAVE
    # ======================================================

    def save(self, commit=True):

        product = super().save(commit=False)

        category = product.category

        # Product Name
        product.product_name = (
            self.cleaned_data.get("product_name") or ""
        ).strip()

        # Sub Category

        subcategory_name = (
            self.cleaned_data.get("subcategory_text") or ""
        ).strip()

        if subcategory_name:

            subcategory, created = (
                SubCategory.objects.get_or_create(
                    category=category,
                    name=subcategory_name
                )
            )

            product.subcategory = subcategory
            product.subcategory_text = subcategory_name

        else:

            product.subcategory = None
            product.subcategory_text = None

        # Brand

        brand_name = (
            self.cleaned_data.get("brand_text") or ""
        ).strip()

        if brand_name:

            brand, created = Brand.objects.get_or_create(
                name=brand_name
            )

            product.brand = brand

        else:

            product.brand = None

        # Thickness

        thickness_name = (
            self.cleaned_data.get("thickness_text") or ""
        ).strip()

        if thickness_name:

            thickness, created = Thickness.objects.get_or_create(
                name=thickness_name
            )

            product.thickness = thickness

        else:

            product.thickness = None

        # Colour

        colour_name = (
            self.cleaned_data.get("colour_text") or ""
        ).strip()

        if colour_name:

            colour, created = Colour.objects.get_or_create(
                name=colour_name
            )

            product.colour = colour

        else:

            product.colour = None

        # Design

        design_name = (
            self.cleaned_data.get("design_text") or ""
        ).strip()

        if design_name:

            design, created = Design.objects.get_or_create(
                name=design_name
            )

            product.design = design

        else:

            product.design = None

        # NOS (Category 3)
        product.nos = self.cleaned_data.get("nos")

        if commit:
            product.save()

        return product
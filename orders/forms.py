from django import forms
from .models import Order, Category

# Change this import if your Customer model is in a different app
from customers.models import Customer


class OrderForm(forms.ModelForm):

    # ======================================================
    # CUSTOMER DROPDOWN
    # ======================================================

    customer_name = forms.ModelChoiceField(
        queryset=Customer.objects.all().order_by("customer_name"),
        required=True,
        empty_label="Select Customer",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "customer_name",
            }
        ),
    )

    # ======================================================
    # CATEGORY
    # ======================================================

    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        required=True,
        empty_label="Select Category",
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "category",
            }
        ),
    )


    

    # ======================================================
    # WIDTH DROPDOWN
    # ======================================================

    width_ft = forms.ChoiceField(
        choices=[
            ("", "Select Width")
        ],
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "width_ft",
            }
        ),
    )

    # ======================================================
    # META
    # ======================================================

    class Meta:

        model = Order

        fields = "__all__"

        widgets = {

            # ==================================================
            # LOCATION
            # ==================================================

            "location": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "location",
                }
            ),

            # ==================================================
            # PRODUCT DETAILS
            # ==================================================

            "subcategory": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "subcategory",
                }
            ),

            "thickness": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "thickness",
                }
            ),

            "design": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "design",
                }
            ),

            "colour": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "colour",
                }
            ),

            "brand": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "brand",
                }
            ),

            "product": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "product",
                }
            ),


            # ==================================================
            # ORDER DETAILS
            # ==================================================

            "width_meter": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "width_meter",
                    "step": "0.01",
                    "readonly": "readonly",
                }
            ),

            "length_ft": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "length_ft",
                    "step": "0.01",
                    "placeholder": "Enter Length",
                }
            ),

            "sheets": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "sheets",
                    "min": "1",
                    "placeholder": "Enter Number of Products",
                }
            ),

            "sq_mtr": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "sq_mtr",
                    "step": "0.01",
                    "readonly": "readonly",
                }
            ),

            "sqm_price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "sqm_price",
                    "step": "0.01",
                    "readonly": "readonly",
                }
            ),

            "rate": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "id": "rate",
                    "step": "0.01",
                    "placeholder": "Enter Rate",
                }
            ),

            "size_text": forms.TextInput(
    attrs={
        "class": "form-control",
        "id": "size_text",
        "placeholder": "Enter Size",
    }
),
            # ==================================================
            # OTHER DETAILS
            # ==================================================

            "loading_from": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "loading_from",
                }
            ),

            "remarks": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "id": "remarks",
                    "rows": 3,
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                    "id": "status",
                }
            ),
        }

# ======================================================
    # INITIALIZE
    # IMPORTANT: THIS MUST BE INSIDE OrderForm CLASS
    # ======================================================

    def __init__(self, *args, **kwargs):

        categories = kwargs.pop("categories", None)

        super().__init__(*args, **kwargs)

        # ==================================================
        # CUSTOMER
        # ==================================================

        self.fields["customer_name"].queryset = (
            Customer.objects.all().order_by("customer_name")
        )

        # ==================================================
        # CATEGORY
        # ==================================================

        if categories is not None:

            self.fields["category"].queryset = categories

        else:

            self.fields["category"].queryset = (
                Category.objects.all().order_by("name")
            )

        # ==================================================
        # DEPENDENT DROPDOWNS
        # ==================================================

        category_id = self.data.get("category")

        if (
            not category_id
            and self.instance.pk
            and self.instance.category
        ):
            category_id = self.instance.category.id


        # ==================================================
        # SUBCATEGORY
        # ==================================================

        if "subcategory" in self.fields:

            if category_id:

                self.fields["subcategory"].queryset = (
                    self.fields["subcategory"]
                    .queryset
                    .model
                    .objects
                    .filter(category_id=category_id)
                )

            else:

                self.fields["subcategory"].queryset = (
                    self.fields["subcategory"]
                    .queryset
                    .model
                    .objects
                    .none()
                )


        # ==================================================
        # THICKNESS
        # ==================================================

        if "thickness" in self.fields:

            self.fields["thickness"].queryset = (
                self.fields["thickness"]
                .queryset
                .model
                .objects
                .all()
            )


        # ==================================================
        # DESIGN
        # ==================================================

        if "design" in self.fields:

            self.fields["design"].queryset = (
                self.fields["design"]
                .queryset
                .model
                .objects
                .all()
            )


        # ==================================================
        # COLOUR
        # ==================================================

        if "colour" in self.fields:

            self.fields["colour"].queryset = (
                self.fields["colour"]
                .queryset
                .model
                .objects
                .all()
            )


        # ==================================================
        # BRAND
        # ==================================================

        if "brand" in self.fields:

            self.fields["brand"].queryset = (
                self.fields["brand"]
                .queryset
                .model
                .objects
                .all()
            )


        # ==================================================
        # PRODUCT
        # ==================================================

        if "product" in self.fields:

            self.fields["product"].queryset = (
                self.fields["product"]
                .queryset
                .model
                .objects
                .all()
            )


        # ==================================================
        # WIDTH FT
        # ==================================================

        submitted_width = self.data.get("width_ft")

        if submitted_width:

            self.fields["width_ft"].choices = [
                ("", "Select Width"),
                (submitted_width, submitted_width),
            ]

        elif (
            self.instance.pk
            and self.instance.width_ft is not None
        ):

            width_value = str(self.instance.width_ft)

            self.fields["width_ft"].choices = [
                ("", "Select Width"),
                (width_value, width_value),
            ]

        else:

            self.fields["width_ft"].choices = [
                ("", "Select Width")
            ]


        # ==================================================
        # DISPATCH STATUS
        # ==================================================

        if "dispatch_status" in self.fields:

            self.fields["dispatch_status"].required = False
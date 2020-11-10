from typing import List, Literal, Optional

from pydantic import BaseModel, HttpUrl


class ReceiptElements(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/receipt#elements
    """

    title: str
    subtitle: Optional[str]
    quantity: Optional[int]
    price: float
    currency: Optional[str]
    image_url: Optional[HttpUrl]


class Address(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/receipt#address
    """

    street_1: str
    street_2: Optional[str]
    city: str
    postal_code: str
    state: str
    country: str


class Summary(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/receipt#summary
    """

    subtotal: Optional[float]
    shipping_cost: Optional[float]
    total_tax: Optional[float]
    total_cost: float


class Adjustments(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/receipt#adjustments
    """

    name: str
    amount: float


class PayloadReceipt(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/receipt
    """

    template_type: Literal["receipt"]
    sharable: Optional[bool]
    recipient_name: str
    merchant_name: Optional[str]
    order_number: str
    currency: str
    payment_method: str  # This can be a custom string, such as, "Visa 1234".
    timestamp: Optional[str]
    elements: Optional[List[ReceiptElements]]
    address: Optional[Address]
    summary: Summary
    adjustments: Optional[List[Adjustments]]

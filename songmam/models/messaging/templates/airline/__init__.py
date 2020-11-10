from typing import List, Literal, Optional

from pydantic import BaseModel


class AuxiliaryFields(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/airline-boarding-pass#auxiliary_field
    """

    label: str
    value: str


class SecondaryFields(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/airline-boarding-pass#secondary_field
    """

    label: str
    value: str


class DepartureAirport(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/airline-itinerary#departure_airport
    """

    airport_code: str
    city: str
    terminal: str
    gate: str


class ArrivalAirport(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/airline-itinerary#arrival_airport
    """

    airport_code: str
    city: str


class FlightSchedule(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/airline-itinerary#flight_schedule
    """

    boarding_time: Optional[str]
    departure_time: str
    arrival_time: Optional[str]


class FlightInfo(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/airline-itinerary#flight_info
    """

    flight_number: str
    departure_airport: DepartureAirport
    arrival_airport: ArrivalAirport
    flight_schedule: FlightSchedule


class BoardingPass(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/airline-boarding-pass#boarding_pass
    """

    passenger_name: str
    pnr_number: str
    travel_class: Optional[str]
    seat: Optional[str]
    auxiliary_fields: Optional[List[AuxiliaryFields]]
    secondary_fields: Optional[List[SecondaryFields]]
    logo_image_url: str
    header_image_url: Optional[str]
    header_text_field: Optional[
        str
    ]  # in ref is "field" /// Optional. Text for the header field.
    qr_code: Optional[str]  # Not available if barcode_image_urlis used.
    barcode_image_url: Optional[str]  # Not available if qr_code is used.
    above_bar_code_image_url: Optional[str]
    flight_info: FlightInfo


class PayloadAirlineBoardingPass(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/airline-boarding-pass
    """

    template_type: Literal["airline_boardingpass"]
    intro_message: str
    locale: str
    theme_color: Optional[str]
    boarding_pass: List[BoardingPass]


class PayloadAirlineCheckin(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/airline-checkin
    """

    template_type: Literal["airline_checkin"]
    intro_message: str
    locale: str
    pnr_number: Optional[str]
    checkin_url: str
    flight_info: List[FlightInfo]


class PassengerInfo(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/airline-itinerary#passenger_info
    """

    passenger_id: str
    ticket_number: Optional[str]
    name: str


class ProductInfo(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/airline-itinerary#product_info
    """

    title: str
    value: str


class PassengerSegmentInfo(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/airline-itinerary#passenger_segment_info
    """

    segment_id: str
    passenger_id: PassengerInfo
    seat: str
    seat_type: str
    product_info: Optional[
        List[ProductInfo]
    ]  # List of products the passenger purchased. Maximum of 4 items is supported.


class PriceInfo(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/airline-itinerary#price_info
    """

    title: str
    amount: int
    currency: Optional[str]


class PayloadAirlineItinerary(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/airline-itinerary
    """

    template_type: Literal["airline_itinerary"]
    intro_message: str
    locale: str
    theme_color: Optional[str]
    pnr_number: str
    passenger_info: List[PassengerInfo]
    flight_info: List[FlightInfo]
    passenger_segment_info: List[PassengerSegmentInfo]
    price_info: Optional[List[PriceInfo]]
    base_price: Optional[int]
    tax: Optional[int]
    total_price: int
    currency: str


class UpdateFlightInfo(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/airline-flight-update#update_flight_info
    """

    flight_number: str
    departure_airport: DepartureAirport
    arrival_airport: ArrivalAirport
    flight_schedule: FlightSchedule


class PayloadAirlineUpdate(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/airline-flight-update#payload
    """

    template_type: Literal["airline_update"]
    intro_message: str
    theme_color: Optional[str]
    update_type: Literal["delay", "gate_change", "cancellation"]
    locale: str
    pnr_number: Optional[str]
    update_flight_info: UpdateFlightInfo

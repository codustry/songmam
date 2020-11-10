import pytest
from songmam.api.content import (
    ContentButton,
    ContentGeneric,
    ContentMedia,
    ContentReceipt,
)
from songmam.models.messaging.templates import (
    Address,
    Adjustments,
    ReceiptElements,
    Summary,
)
from songmam.models.messaging.templates.button import (
    CallButton,
    LogInButton,
    LogOutButton,
    PostbackButton,
    URLButton,
)
from songmam.models.messaging.templates.generic import GenericElement
from songmam.models.messaging.templates.media import MediaElement
from songmam.models.webhook.events.messages import Sender


@pytest.fixture
def page():
    return Page()


@pytest.fixture
def test_user():
    # Tan
    return Sender(id="2945944152161824")


@pytest.mark.asyncio
async def test_send(test_user):
    buttons1 = [
        URLButton(
            title="Open Webview",
            url="https://www.youtube.com/watch?v=riYzZrkOc3o",
            messenger_extensions=False,
        ),
        PostbackButton(title="trigger Postback", payload="print is true"),
        CallButton(title="Call Phone Number", payload="+66900622693"),
    ]
    content_button_template = ContentButton(
        text=f"replied to ", buttons=buttons1, quick_replies=None
    )
    # ------------------------------------------------------------------- #
    default_act = DefaultAction(
        # url="https://www.youtube.com/watch?v=jrOUGFFtMCw",
        # fallback_url="https://frankonfraud.com/wp-content/uploads/2018/11/fallback-fraud-in-us.jpg"
        url="https://www.youtube.com/watch?v=jrOUGFFtMCw",
    )
    buttons2 = [
        LogInButton(
            url="https://www.youtube.com/watch?v=riYzZrkOc3o",
        ),
        LogOutButton(),
    ]
    gallery = [
        GenericElement(
            title="Welcome to Generic (/w DA)",
            subtitle="subtitle is here!",
            image_url="https://www.biospectrumasia.com/uploads/articles/is-japan-changing-its-attitude-towards"
            "-generic-drugs.jpg",
            default_action=default_act,
            buttons=None,
        ),
        GenericElement(
            title="Button Test",
            subtitle="Log I/O sub-",
            image_url="https://www.biospectrumasia.com/uploads/articles/is-japan-changing-its-attitude-towards"
            "-generic-drugs.jpg",
            default_action=DefaultAction(
                url="https://developers.facebook.com/docs/messenger-platform/reference/templates/generic#elements"
            ),
            buttons=buttons2,
        ),
    ]
    content_generic_template = ContentGeneric(
        elements=gallery,
        image_aspect_ratio="square",  # "horizontal" or "square"
        quick_replies=None,
    )
    # ------------------------------------------------------------------- #
    buttons3 = [
        URLButton(
            title="What is this?!?!",
            url="https://www.facebook.com/sirote.klampaiboon/photos/a.373530246050409/4230721946997867/",
        )
    ]
    buttons4 = [
        URLButton(
            title="What is this?!?!",
            url="https://www.republicworld.com/entertainment-news/whats-viral/video-of-squirrel-asking-for-water"
            "-leaves-netizens-heartbroken-watch.html ",
        ),
        URLButton(
            title="Original",
            url="https://www.facebook.com/1588173658083515/videos/301934891007397/",
        ),
    ]
    media1 = [
        MediaElement(
            media_type="image",
            url="https://www.facebook.com/sirote.klampaiboon/photos/a.373530246050409/4230721946997867/",
            buttons=buttons3,
        )
    ]
    media2 = [
        MediaElement(
            media_type="video",
            url="https://www.facebook.com/1588173658083515/videos/301934891007397/",
            buttons=buttons4,
        )
    ]
    content_media_image_template = ContentMedia(
        elements=media1,
        sharable=False,  # Visible next to the content in mobile messenger
        quick_replies=None,
    )
    content_media_video_template = ContentMedia(
        elements=media2, sharable=True, quick_replies=None
    )
    # ------------------------------------------------------------------- #
    address_rec = Address(
        street_1="Address 1",
        street_2="Address 2",
        city="City",
        postal_code="10140",
        state="state",
        country="country",
    )
    summary_rec = Summary(
        subtotal=75.00,
        shipping_cost=4.95,
        total_tax=6.19,
        total_cost=56.14,
    )
    adjustments_rec = [
        Adjustments(name="New Customer Discount", amount=20),
        Adjustments(name="$10 Off Coupon", amount=10),
    ]
    receipt_element = [
        ReceiptElements(
            title="Elements are here!",
            subtitle="this on is for FREE!!!",
            quantity=2,
            price=50.00,
            currency="USD",
            image_url="https://www.pngjoy.com/pngs/96/2010071_residentsleeper-wutface-emote-png-download.png",
        ),
        ReceiptElements(
            title="!Worker require here!",
            subtitle="Want someone to carry on",
            quantity=1,
            price=25.00,
            currency="USD",
            image_url="https://www.pngjoy.com/pngs/96/2010071_residentsleeper-wutface-emote-png-download.png",
        ),
    ]
    content_receipt_template = ContentReceipt(
        sharable=True,
        recipient_name="Someone Special",
        merchant_name=None,
        order_number="12345678902",
        currency="USD",
        payment_method="Visa 1234",  # This can be a custom string, such as, "Visa 1234".
        timestamp="1428444852",
        elements=receipt_element,
        address=address_rec,
        summary=summary_rec,
        adjustments=adjustments_rec,
        quick_replies=None,
    )
    # ------------------------------------------------------------------- #
    page.send_sync(test_user, content_button_template)
    page.send_sync(test_user, content_generic_template)
    page.send_sync(test_user, content_media_image_template)
    page.send_sync(test_user, content_media_video_template)
    page.send_sync(test_user, content_receipt_template)

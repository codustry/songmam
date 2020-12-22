import pytest

from songmam.models.messaging.templates.button import PostbackButton, URLButton
from songmam.models.messenger_profile import MenuPerLocale


@pytest.mark.asyncio
async def test_get_profile(api, test_user):
    res = await api.get_user_profile(test_user)
    print(res)


@pytest.mark.asyncio
async def test_set_user_menu(api, test_user):
    menu = MenuPerLocale(
            composer_input_disabled=True,
            call_to_actions=[
                PostbackButton(
                    title="🔎 ค้นหางาน", payload="flows.jobseeker.job_search:start"
                ),
                URLButton(
                    title="😎 โปรไฟล์ของฉัน",
                    url="https://webview-main-prod.onrender.com/user/edit",
                    messenger_extensions=True,
                ),
                PostbackButton(title="⚙️ การตั้งค่า-อื่นๆ", payload="flows:settings"),
            ],
        )
    res = await api.set_user_menu(test_user, menu)
    print(res)

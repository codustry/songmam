<p align="center">
  <a href="https://codustry.com/technologies/songmam">
    <img alt="babel" src="https://storage.googleapis.com/codustry_assets/github/icon-shadow-songmam.png" height="100">
  </a>
</p>


# Songmam

a facebook messenger hypermodern python library based on fastapi. 


<div align="center">

[![Build status](https://github.com/codustry/songmam/workflows/build/badge.svg?branch=master&event=push)](https://github.com/codustry/songmam/actions?query=workflow%3Abuild)
[![Python Version](https://img.shields.io/pypi/pyversions/songmam.svg)](https://pypi.org/project/songmam/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/codustry/songmam/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/codustry/songmam/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/codustry/songmam/releases)
[![License](https://img.shields.io/github/license/codustry/songmam)](https://github.com/codustry/songmam/blob/master/LICENSE)

</div>



## Features

- Async
- based on `Pydantic`, easy to work with `FastApi`
- 1-1 structure to [official facebook documentation](https://developers.facebook.com/docs/messenger-platform/)
- Implement validation and Security Protocals

  
## Installation 

```bash
pip install songmam
```
## Documentation

WIP
<!-- [Documentation](https://linktodocumentation) -->

  
## Usage/Examples

There are a few examples under the folder, `examples`

```python
from fastapi import FastAPI

from songmam import WebhookHandler, MessengerApi
from songmam.models.webhook import MessagesEvent

app = FastAPI(
    title="echo"
)


handler = WebhookHandler(
    app=app, path="/webhook", app_secret=FACEBOOK_APP_SECRET, verify_token=FACEBOOK_PAGE_VERIFY_TOKEN
)

api = MessengerApi(access_token=FACEBOOK_PAGE_ACCESS_TOKEN)


@handler.add(MessagesEvent)
async def handle_message(event: MessagesEvent, *args, **kwargs):
    """
    echo back message
    """
    await api.send(event.theMessaging.sender, event.theMessaging.message.text)

```

  
## Used By

This project is used by the following companies:

- Codustry
  - [Gebwai](https://gebwai.com/)
  - [Saku Chatbot](https://saku.freaklab.org/)

  
## Authors

- [@circleoncircles](https://www.github.com/circleoncircles)

  
## Feedback

If you have any feedback, you can create an issue or PR.

  

## 🛡 License

[![License](https://img.shields.io/github/license/codustry/songmam)](https://github.com/codustry/songmam/blob/master/LICENSE)

This project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/codustry/songmam/blob/master/LICENSE) for more details.


## Credits

This project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template).

# Echo Chatbot 👋

Bot that echo back the text user type in

## 🏫 How to use

1. You need to have a facebook app set up. Go to [Facebook for Developers](https://developers.facebook.com/apps/) and create a messenger app.
    1. Get "Access Token", 
    2. Set "Verify Token", you could set this to any predefined text. 
    3. Get "App Secret"
2. Set them as environement variables. Pick one
    1. set variables in a `.env` file. (There is a `.env.sample` template file. Just copy and rename it! 👨)
    2. use shell command to set e.g. `export FACEBOOK_PAGE_VERIFY_TOKEN=xxx` 
3. Set up Python Environment using `Pipfile` via [`pipenv install` cli](https://github.com/pypa/pipenv)
4. Expose localhost using [`ngrok http 8000`](https://ngrok.com/) and obtain the 'forwarding URL` e.g. https://7354337cdd53.ngrok.io
5. Go to [Facebook for Developers](https://developers.facebook.com/apps/) and set `Callback URL` to `forward URL` + `/webhook` e.g. `https://7354337cdd53.ngrok.io/webhook`
6. Run `pyenv run python main.py`

### FAQ
**Where is access token and verify token?**

At the sidebar, App > Products.Messenger > Settings. Look at the "Access Tokens" section.
For the verify token, it is just a section below.

**Where is App Secret?**

At the sidebar, App > Settings > Basic. Look at the first section.

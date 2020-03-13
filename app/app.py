from flask import Flask, g, redirect, url_for
from flask_oidc import OpenIDConnect
from okta import UsersClient

app = Flask(__name__)
app.config["OIDC_CLIENT_SECRETS"] = "client_secrets.json"
app.config["OIDC_COOKIE_SECURE"] = False
app.config["OIDC_CALLBACK_ROUTE"] = "/home"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
app.config["SECRET_KEY"] = "longrandomstring"
oidc = OpenIDConnect(app)
okta_client = UsersClient("https://dev-322395.okta.com", "00NTRtMajPFUzLLpHbVYl6ZufW_nazSJkOotrmZCLq")

@app.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = okta_client.get_user(oidc.user_getfield("sub"))
    else:
        g.user = None

@app.route("/home")
def hello():
    return """
    <h1>Python Flask in Docker!</h1>
    <p> A sample web-app for running Flask inside Docker.</p>
    """
@app.route("/dashboard")
@oidc.require_login
def dashboard():
    return "Dashboard"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

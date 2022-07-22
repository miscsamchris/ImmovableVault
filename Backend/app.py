from ImmovableVault import app, db, redirect, url_for, LoginManager
from flask_login import login_required, current_user, logout_user, login_user

from ImmovableVault.Models import UserProfile

login_manager = LoginManager()
login_manager.login_view = "Endpoints.LoginUser"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    user = UserProfile.query.filter_by(id=id).first()
    if user:
        return user
    return None


@app.route("/")
def home():
    return redirect(url_for("Endpoints.LoginUser"))


if __name__ == "__main__":
    db.create_all()
    app.run(threaded=True, port=80)

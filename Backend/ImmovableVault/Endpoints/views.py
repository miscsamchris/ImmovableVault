import imp
import requests
import json
import sys
from datetime import datetime, date
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    jsonify,
    send_from_directory,
)
from flask_login import login_required, current_user, logout_user, login_user
from ImmovableVault.Models import Document, DocumentAccess, UserProfile
from ImmovableVault import db
import hashlib
from werkzeug.utils import secure_filename

from datetime import date, timedelta
import os

endpoints_blueprint = Blueprint(
    "Endpoints", __name__, template_folder="templates", static_folder="static"
)


@endpoints_blueprint.route("/logincheck", methods=["GET", "POST"])
def LoginUser():
    if current_user.is_authenticated == True:
        return jsonify({"code": 200})
    else:
        return jsonify({"code": 400})


@endpoints_blueprint.route("/Authenticate", methods=["GET", "POST"])
def Authenticate():
    if request.method == "POST":
        user_unique_id = request.form.get("user_unique_id")
        user = UserProfile.query.filter_by(user_unique_id=user_unique_id).first()
        if user == None:
            tempuser = UserProfile("", user_unique_id, "", "")
            db.session.add(tempuser)
            db.session.commit()
            return jsonify({"code": 201})
        if user.user_email == "" and user.user_name == "":
            return jsonify({"code": 201})
        else:
            login_user(user)
            return jsonify({"code": 200})


@endpoints_blueprint.route("/Register", methods=["GET", "POST"])
def Register():
    if request.method == "POST":
        user_name = request.form.get("user_name")
        user_unique_id = request.form.get("user_unique_id")
        user_email = request.form.get("user_email")
        user_password = request.form.get("user_password")
        user = UserProfile.query.filter_by(user_unique_id=user_unique_id).first()
        if user != None:
            user.user_name = user_name
            user.user_email = user_email
            user.user_password = user_password
            db.session.commit()
            return jsonify({"code": 200})
        else:
            return jsonify({"code": 500})


@endpoints_blueprint.route("/CreateDocument", methods=["GET", "POST"])
def CreateDocument():
    if request.method == "POST":
        document_name = request.form.get("document_name")
        user_unique_id = request.form.get("user_unique_id")
        document_type = request.form.get("document_type")
        document_path = request.form.get("document_path")
        user = UserProfile.query.filter_by(user_unique_id=user_unique_id).first()
        if request.form != {} and user != None and document_type == "Upload":
            UserDocument = request.files["Document"]
            path = f"{endpoints_blueprint.root_path}/static/Documents/"
            path = path.replace("\\", "/")
            hashname = abs(hash(document_name + user_unique_id)) % (10**8)
            os.makedirs(path + str(hashname) + "/" + "Files/", exist_ok=True)
            UserDocumentfilename = secure_filename(UserDocument.filename)
            UserDocument.save(
                os.path.join(
                    path + str(hashname) + "/" + "Files/", UserDocumentfilename
                )
            )
            document_path = "http://localhost/backend/download/" + str(hashname) + "/"
            document = Document(
                document_name, str(hashname), document_type, document_path
            )
            db.session.add(document)
            user.documents.append(document)
            db.session.commit()
            return jsonify({"code": 200})
        if request.form != {} and user != None and document_type != "upload":
            hashname = abs(hash(document_name + user_unique_id)) % (10**8)
            document = Document(
                document_name, str(hashname), document_type, document_path
            )
            db.session.add(document)
            user.documents.append(document)
            db.session.commit()
            return jsonify({"code": 200})
        else:
            return jsonify({"code": 500})


@endpoints_blueprint.route("/CreateAccess", methods=["GET", "POST"])
def CreateAccess():
    if request.method == "POST":
        document_id = request.form.get("document_id")
        access_type = request.form.get("access_type")
        access_to_id = request.form.get("access_to_id")
        document = Document.query.filter_by(id=document_id).first()
        if request.form != {} and document != None:
            time_now = date.today()
            time_deadline = time_now + timedelta(seconds=int(access_type))
            access = DocumentAccess(
                document.document_name,
                time_now,
                time_deadline,
                access_type,
                access_to_id,
            )
            db.session.add(access)
            document.Accesses.append(access)
            db.session.commit()
            return jsonify({"code": 200})
        else:
            return jsonify({"code": 500})


@endpoints_blueprint.route("/ViewDocuments", methods=["GET", "POST"])
def ViewDocuments():
    if request.method == "POST":
        user_unique_id = request.form.get("user_unique_id")
        user = UserProfile.query.filter_by(user_unique_id=user_unique_id).first()
        if request.form != {} and user != None:
            time_now = date.today()
            data = [
                {
                    "id": x.id,
                    "name": x.document_name,
                    "url": x.document_path,
                    "type": "Owned",
                }
                for x in user.documents
            ]
            sharedata = DocumentAccess.query.all()
            data.extend(
                [
                    {
                        "id": x.id,
                        "name": x.document_name,
                        "url": x.Document.document_path,
                        "type": "Shared",
                    }
                    for x in sharedata
                    if x.access_to_id == user_unique_id
                    and date.fromisoformat(x.access_deadline) >= time_now
                ]
            )
            if data != []:
                return jsonify(
                    {
                        "code": 200,
                        "data": data,
                    }
                )
            else:
                return jsonify(
                    {
                        "code": 201,
                    }
                )
        else:
            return jsonify({"code": 500})


@endpoints_blueprint.route("/Logout", methods=["GET", "POST"])
def Logout():
    logout_user()
    return jsonify({"code": 200})


@endpoints_blueprint.route("/download/<string:id>/", methods=["GET", "POST"])
def stream(id):
    path_actual = f"{endpoints_blueprint.root_path}/static/Documents/{id}/Files"
    path = path_actual
    filename = os.listdir(path_actual)[0]
    return send_from_directory(path, filename, as_attachment=True)

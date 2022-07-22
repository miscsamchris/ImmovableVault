import UAuth from '@uauth/js'

const uauth = new UAuth({
  clientID: '7abd0295-6373-423c-bdd9-a9742a67855d',
  redirectUri: 'http://localhost:5000/callback',
})
var userUnique_id = ""
var loginbtn = document.getElementById("Login");
var logoutbtn = document.getElementById("Logout");
var creatdocumentbtn = document.getElementById("CreateDocument");
var ShareDocumenttbtn = document.getElementById("CreateAccess");
var maincontent = document.getElementById("main-content");
loginbtn.onclick = async () => {
  try {
    const authorization = await uauth.loginWithPopup()
    console.log(authorization)
    userUnique_id = authorization["idToken"]["sub"];
    const Http = new XMLHttpRequest();
    const url = 'http://localhost/backend/Authenticate';
    Http.open("POST", url);
    Http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    Http.send("user_unique_id=" + userUnique_id);
    Http.onload = (e) => {
      var rawdata = Http.responseText.toString()
      console.log(rawdata);
      data = JSON.parse(rawdata);
      if (data["code"] == 200) {
        loginbtn.innerHTML = "Welcome, " + userUnique_id;
        maincontent.style.display = "block";
        loadtabledate();
      }
      else if (data["code"] == 201) {
        var locModal = document.getElementById('CreateReferral');
        locModal.style.display = "block";
        locModal.className = "modal show";
      }
    }
  } catch (error) {
    console.error(error)
  }
}
var registerbtn = document.getElementById("RegisterUser");
registerbtn.onclick = async () => {
  try {
    var locModal = document.getElementById('CreateReferral');
    locModal.style.display = "block";
    locModal.className = "modal hide";
    var UserName = document.getElementById("UserName").value.toString();
    var UserEmail = document.getElementById("UserEmail").value.toString();
    var UserPassword = document.getElementById("UserPassword").value.toString();
    const Http = new XMLHttpRequest();
    const url = 'http://localhost/backend/Register';
    Http.open("POST", url);
    Http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    var data = "user_unique_id=" + userUnique_id + "&user_name=" + UserName + "&user_email=" + UserEmail + "&user_password=" + UserPassword;
    Http.send(data);
    Http.onload = (e) => {
      console.log(Http.responseText);
      var rawdata = Http.responseText.toString()
      data = JSON.parse(rawdata);
      if (data["code"] == 200) {
        loginbtn.innerHTML = "Welcome, " + userUnique_id;
        maincontent.style.display = "block";
        loadtabledate();
      }
      else if (data["code"] == 500) {
        console.error("error")
      }
    }
  } catch (error) {
    console.error(error)
  }
}

logoutbtn.onclick = async () => {
  await uauth.logout()
  const Http = new XMLHttpRequest();
  const url = 'http://localhost/backend/Logout';
  Http.open("POST", url);
  Http.send();
  Http.onload = (e) => {
    console.log(Http.responseText);
    var rawdata = Http.responseText.toString()
    data = JSON.parse(rawdata);
    if (data["code"] == 200) {
      console.log('Logged out with Unstoppable')
      maincontent.style.display = "none";
      loginbtn.innerHTML = "Login with Unstoppable";
    }
    else if (data["code"] == 500) {
      console.error("error")
    }
  }
}

creatdocumentbtn.onclick = async () => {
  try {
    var document_name = document.getElementById("document_name").value.toString();
    var document_type = document.getElementById("document_type").value.toString();
    var document_path = document.getElementById("document_path").value.toString();
    var file = document.getElementById("Document").files[0];
    const Http = new XMLHttpRequest();
    const url = 'http://localhost/backend/CreateDocument';
    Http.open("POST", url, true);
    var formData = new FormData();
    formData.append("Document", file);
    formData.append("user_unique_id", userUnique_id);
    formData.append("document_name", document_name);
    formData.append("document_type", document_type);
    formData.append("document_path", document_path);
    Http.send(formData);
    Http.onload = (e) => {
      console.log(Http.responseText);
      var rawdata = Http.responseText.toString()
      data = JSON.parse(rawdata);
      if (data["code"] == 200) {
        loadtabledate()
      }
      else if (data["code"] == 500) {

      }
    }
  } catch (error) {
    console.error(error)
  }
}

ShareDocumenttbtn.onclick = async () => {
  try {
    var document_id = document.getElementById("document_id").value.toString();
    var access_type = document.getElementById("access_type").value.toString();
    var access_to_id = document.getElementById("access_to_id").value.toString();
    const Http = new XMLHttpRequest();
    const url = 'http://localhost/backend/CreateAccess';
    Http.open("POST", url);
    Http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    var data = "document_id=" + document_id + "&access_type=" + access_type + "&access_to_id=" + access_to_id;
    Http.send(data);
    Http.onload = (e) => {
      console.log(Http.responseText);
      var rawdata = Http.responseText.toString()
      data = JSON.parse(rawdata);
      if (data["code"] == 200) {
        console.log("Shared Document");
        var share = document.getElementById("ShareDocument");
        share.style.display = "block";
        share.className = "modal hide";
      }
      else if (data["code"] == 500) {
        console.error("No Document Shared");
      }
    }
  } catch (error) {
    console.error(error)
  }
}

function loadtabledate() {
  const Http = new XMLHttpRequest();
  const url = 'http://localhost/backend/ViewDocuments';
  Http.open("POST", url);
  Http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  Http.send("user_unique_id=" + userUnique_id);
  Http.onload = (e) => {
    var rawdata = Http.responseText.toString()
    data = JSON.parse(rawdata);
    console.log(data);
    if (data["code"] == 200) {
      var mydocuments = data["data"]
      for (var i = 0; i < mydocuments.length; i++) {
        if (mydocuments[i].type == "Shared") {
          var DownBtn = document.createElement("a");
          DownBtn.innerHTML = "Download";
          DownBtn.href = mydocuments[i].url;
          DownBtn.target = "_blank";
          DownBtn.classList.add("btn", "btn-primary", "mb-3", "mr-sm-2")
          var tbod = document.getElementById("UserDocuments")
          var newRow = tbod.insertRow();
          var filename = newRow.insertCell();
          var filenameText = document.createTextNode(mydocuments[i].name);
          filename.appendChild(filenameText);
          var actions = newRow.insertCell();
          actions.appendChild(DownBtn);
        }
        else {
          var Sharebtn = document.createElement("button");
          Sharebtn.innerHTML = "Share";
          Sharebtn.id = mydocuments[i].id
          Sharebtn.onclick = function () {
            ShareDocument(this.id)
          }
          Sharebtn.classList.add("btn", "btn-primary", "mb-3", "mr-sm-2")
          var tbod = document.getElementById("UserDocuments")
          var newRow = tbod.insertRow();
          var filename = newRow.insertCell();
          var filenameText = document.createTextNode(mydocuments[i].name);
          filename.appendChild(filenameText);
          var fileurl = newRow.insertCell();
          var DownBtn = document.createElement("a");
          DownBtn.innerHTML = "Download";
          DownBtn.href = mydocuments[i].url;
          DownBtn.target = "_blank";
          DownBtn.classList.add("btn", "btn-primary", "mb-3", "mr-sm-2")
          fileurl.appendChild(DownBtn);
          var actions = newRow.insertCell();
          actions.appendChild(Sharebtn);
        }
      }
    }
    else if (data["code"] == 500) {
      console.error("error")
    }
  }
}
function ShareDocument(doucment_id) {
  var share = document.getElementById("ShareDocument");
  var did = document.getElementById("document_id");
  did.value = doucment_id;
  share.style.display = "block";
  share.className = "modal show";
}
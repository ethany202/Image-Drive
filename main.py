from flask import Flask, redirect, url_for, render_template, request, session, g
from datetime import timedelta
from werkzeug.utils import secure_filename
from PIL import Image
import os
import retrieveData


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "ved"
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
    return app


app = create_app()
image_formats = [".jpg", ".jpeg", ".png", ".gif", ".tiff"]
current_dir = os.path.dirname(__file__)


@app.route('/home')
def home():
    if g.user:
        return render_template("home.html", name=session['user'])
    else:
        return render_template("home.html", name="Not Logged In")



@app.route("/personal-page")
def redirectToPersonal():
    if g.user:
        return render_template("personalPage.html", name=session['user'])
    else:
        return redirect(url_for('loginPage'))



@app.route("/login", methods=['POST', 'GET'])
def loginPage():
    if g.user:
        current_user = session['user']
    else:
        current_user = "Not Logged In"
    if request.method == "POST":
        session.pop('user', None)
        email = request.form.get("email")
        password = request.form.get("password")
        conn = retrieveData.connect()
        if conn != None:
            user_data = retrieveData.verify_credentials(email, password, conn)
            if len(user_data) == 0:
                retrieveData.close_connection(conn)
                return render_template("loginRedirect.html", name="Not Logged In", error="Username or password is invalid")
            else:
                session.permanent = True
                session['user'] = request.form.get("email")
                retrieveData.close_connection(conn)
                return redirect(url_for("redirectToPersonal", name=session['user']))
    return render_template("loginRedirect.html", name=current_user)



@app.route("/sign-up", methods =["POST", "GET"])
def signupPage():
    if g.user:
        current_user = session['user']
    else:
        current_user = "Not Logged In"
    if request.method == "POST":
        session.pop('user', None)
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        email = request.form.get("email")
        password = request.form.get("password")
        password_confirm = request.form.get("passwordConfirm")
        if password_confirm != password:
            return render_template("signupRedirect.html", name=current_user, error="Please confirm your password")
        conn = retrieveData.connect()
        if conn!=None:
            user_data = retrieveData.check_records(email, conn)
            if len(user_data) != 0:
                print("This email already has an account")
                retrieveData.close_connection(conn)  
                return render_template("signupRedirect.html", name=current_user, error="This email already has an account associated with it")
            else:           
                retrieveData.add_user(first_name, last_name, email, password, conn)
                session['user'] = email
                session.permanent = True
                retrieveData.close_connection(conn)  
                return redirect(url_for("redirectToPersonal", name=current_user))  
    return render_template("signupRedirect.html", name=current_user)



@app.route("/sign-out")
def signoutRedirect():
    g.user = None
    if 'user' in session:
        session.pop('user', None)
    return redirect(url_for("home", name="Not Logged In"))



@app.route("/load-images")
def loadImages():
    if g.user:
        conn = retrieveData.connect()
        if conn!=None:
            user_records = retrieveData.get_images(session['user'], conn)
            print(user_records)
            return render_template("loadImages.html", name=session['user'], boolean="True", imagesArray =user_records)
    return redirect(url_for("loginPage", name="Not Logged In"))



@app.route("/upload-images", methods=["POST", "GET"])
def uploadImages():
    if g.user == None:
        return redirect(url_for("loginPage", name="Not Logged In"))
    if request.method == 'POST':
        image_title = request.form.get("imageTitle")
        file = request.files['file']
        is_image = False
        print(file.filename)
        for formats in image_formats:
            if str(file.filename).find(formats) != -1:
                is_image=True
                break
        if is_image:
            conn = retrieveData.connect()
            if conn!=None:
                ref = rf"\static\personalImages\{session['user']}_{str(file.filename)}"
                save_image(file, ref)
                img = Image.open(current_dir+str(ref));
                img_height = img.size[1]
                img_width = img.size[0]
                retrieveData.add_images(image_title, ref, session['user'], img_width, img_height, conn)
            else:
                return render_template("uploadImages.html", name=session['user'], error="There was an error when uploading the image")
        else:
            return render_template("uploadImages.html", name=session['user'], error="Please upload an image file")
    return render_template("uploadImages.html", name=session['user'])

        

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


def save_image(image, image_reference):
    complete_path = current_dir+str(image_reference) 
    if not os.path.exists(str(complete_path)):
        image.save(complete_path)



if __name__ == "__main__":
    app.run(debug=True)
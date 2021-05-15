from flask import Flask, redirect, url_for, render_template, request
import sites
import retrieveData


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "ved"
    return app


app = create_app()


@app.route('/home')
def home():
    if sites.authenticated:
        return render_template("home.html", name = sites.current_user_data[0])
    else:
        return render_template("home.html", name="Not Logged In")


@app.route("/email=<email>")
def redirectToPersonal(email):
    if sites.authenticated:
        return render_template("personalPage.html", name=sites.current_user_data[0])
    else:
        return redirect(url_for("loginPage"))



@app.route("/login", methods=['POST', 'GET'])
def loginPage():
    if sites.authenticated:
        current_user = sites.current_user_data[0]
    else:
        current_user = "Not Logged In"
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        conn = retrieveData.connect()
        if conn != None:
            user_data = retrieveData.verify_credentials(email, password, conn)
            if len(user_data) == 0:
                print("Incorrect credentials")
                sites.authenticated = False
                retrieveData.close_connection(conn)
                return render_template("loginRedirect.html", name=current_user, error="Error logging in: Username or password is invalid")
            else:
                sites.current_user_data = user_data
                sites.authenticated = True
                print("Logged In...")
                retrieveData.close_connection(conn)
                return redirect(url_for("redirectToPersonal", email=user_data[0], name=current_user))
    return render_template("loginRedirect.html", name=current_user)



@app.route("/sign-up", methods =["POST", "GET"])
def signupPage():
    if sites.authenticated:
        current_user = sites.current_user_data[0]
    else:
        current_user = "Not Logged In"
    if request.method == "POST":
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        email = request.form.get("email")
        password = request.form.get("password")
        password_confirm = request.form.get("passwordConfirm")
        if password_confirm != password:
            return render_template("signupRedirect.html", name=current_user, error="Error Signing Up: Please confirm your password")
        conn = retrieveData.connect()
        if conn!=None:
            user_data = retrieveData.check_records(email, password, conn)
            if len(user_data) != 0:
                print("This email already has an account")
                retrieveData.close_connection(conn)  
                return render_template("signupRedirect.html", name=current_user, error="Error Signing Up: This email already has an account associated with it")
            else:
                sites.authenticated = True
                print("New account has been made")
                sites.current_user_data = user_data
                retrieveData.close_connection(conn)  
                return redirect(url_for("redirectToPersonal", email=user_data[0], name=current_user))  
    return render_template("signupRedirect.html", name=current_user)


@app.route("/sign-out")
def signoutRedirect():
    sites.authenticated = False
    return redirect(url_for("home", name="Not Logged In"))


@app.route("/load-images")
def loadImages():
    if sites.authenticated:
        return render_template("loadImages.html", name=sites.current_user_data[0])
    else:
        return redirect(url_for("loginPage", name="Not Logged In"))

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, redirect, url_for, render_template, request
from sites import sites
import retrieveData


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "ved"
    app.register_blueprint(sites, url_prefix='/')
    return app


app = create_app()
current_user_data = []



@app.route("/email=<email>")
def redirectToPersonal(email):
    if sites.authenticated:
        return render_template("personalPage.html")
    else:
        return redirect(url_for("loginPage"))



@app.route("/login", methods=['POST', 'GET'])
def loginPage():
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
                return render_template("loginRedirect.html")
                # print error message
            else:
                sites.authenticated = True
                print("Logged In...")
                retrieveData.close_connection(conn)
                return redirect(url_for("redirectToPersonal", email=user_data[0]))
    return render_template("loginRedirect.html")



@app.route("/sign-up", methods =["POST", "GET"])
def signupPage():
    if request.method == "POST":
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        email = request.form.get("email")
        password = request.form.get("password")
        conn = retrieveData.connect()
        if conn!=None:
            user_data = retrieveData.check_records(email, password, conn)
            if len(user_data) != 0:
                print("This email already has an account")
                #return
            else:
                sites.authenticated = True
                print("New account has been made")
                return redirect(url_for("redirectToPersonal", email=user_data[0]))
        retrieveData.close_connection(conn)   
    return render_template("signupRedirect.html")



if __name__ == "__main__":
    app.run(debug=True)
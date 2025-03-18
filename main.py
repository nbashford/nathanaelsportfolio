from flask import Flask, render_template, request, send_from_directory
from flask_bootstrap import Bootstrap5
import os
import email_funct

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")
bootstrap = Bootstrap5(app)
email_funct.setup_email_config(app) # set up email flask configuration


@app.route('/', methods=["POST", "GET"])
def homepage():
    """load the main homepage - if contact form entered - send contact details to email_funct to send."""
    sent = None
    if request.method == 'POST':
        name = request.form['nameInput']
        email = request.form['emailInput']
        message = request.form['message']
        sent = email_funct.send_email(name, email, message)

    # return render_template('strata.html', email_sent=sent)
    return render_template('homepage.html', email_sent=sent)


@app.route('/download-cv')
def download_cv():
    return send_from_directory('static/downloads',
                               'NathanaelBashfordCV.pdf',
                               as_attachment=True)



if __name__ == "__main__":
    app.run()

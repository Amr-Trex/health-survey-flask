from flask import Flask, request, jsonify, render_template, url_for
from dataProcessing import check_data, send_email

app = Flask(__name__)




# Route to render the HTML form
@app.route('/')
def index():
    return render_template('index.html')  # Ensure 'index.html' is in a 'templates' folder


@app.route('/submit', methods=['POST'])
def submit():
    data = request.form
    checked_data = check_data(data)
    send_email(checked_data)
    
    print(checked_data)

    return render_template('ThankYouPage.html')




if __name__ == '__main__':
    # The following line is only for development purposes. In production, you should use a proper WSGI server.
    # If you don't know what a WSGI server is, here's a brief explanation:
    # WSGI stands for Web Server Gateway Interface, which is a standard interface for web servers to communicate with web applications.
    # A WSGI server is a server that can run a WSGI application (like this Flask app) and serve it to the outside world.
    # Gunicorn is a popular WSGI server that is commonly used in production environments.
    # To run this app in production, you would typically use a command like `gunicorn -w 4 app:app` (replace `app` with the name of your Flask app).
    # This will start a Gunicorn server with 4 worker processes that can handle incoming requests concurrently.
    # If you want to use a different WSGI server, you can do so by replacing `gunicorn` with the name of the server you want to use.
    # But for development purposes, the following line is fine.
    app.run(debug=True)


from app import app, mongo
from routes.views import views



app.register_blueprint(views, url_prefix='/')

ssl_context = (".\\cert\\fullchain.pem", ".\\cert\\privkey.pem")

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=443, ssl_context=ssl_context)

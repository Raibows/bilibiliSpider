from FlaskServer.app import create_app
from Config import flaskserver_config
app = create_app()




default_flask_server_host = flaskserver_config.flaskserver_host
default_flask_server_port = flaskserver_config.flaskserver_port
default_flask_server_threaded = flaskserver_config.flaskserver_threaded


if __name__ == '__main__':
    app.run(
        host=default_flask_server_host,
        port=default_flask_server_port,
        threaded=True
    )
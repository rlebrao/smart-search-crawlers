from flask import Flask

def create_app(config_file):
    app = Flask(__name__, )
    app.config.from_object(config_file)
    return app
    
if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True)

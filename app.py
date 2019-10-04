from flask import Flask
from flask_restful import Resource, Api

from resources.Arpenp import Arpenp
from resources.Cadesp import Cadesp
from resources.Caged import Caged
from resources.Censec import Censec
from resources.Detran import Detran
from resources.Infocrim import Infocrim

app = Flask(__name__)
api = Api(app)

#Route
api.add_resource(Arpenp,'/arpenp')
# api.add_resource(Cadesp,'/cadesp')
api.add_resource(Caged, '/caged')
api.add_resource(Censec, '/censec')
api.add_resource(Detran, '/detran')
api.add_resource(Infocrim, '/infocrim')

if __name__ == "__main__":
    app.run(debug=False)
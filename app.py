from flask import Flask
from flask_restful import Resource, Api

from resources.Arisp import Arisp
from resources.Arpenp import Arpenp
from resources.Cadesp import Cadesp
from resources.Caged import Caged
from resources.Censec import Censec
from resources.Detran import Detran
from resources.Infocrim import Infocrim
from resources.Juscesp import Jucesp
from resources.Siel import Siel
from resources.Sivec import Sivec
from resources.BolsaFamilia import BolsaFamilia

app = Flask(__name__)
api = Api(app)

#Route
api.add_resource(Arisp, '/arisp')
api.add_resource(Arpenp,'/arpenp')
api.add_resource(Cadesp,'/cadesp')
api.add_resource(Caged, '/caged')
api.add_resource(Censec, '/censec')
api.add_resource(Detran, '/detran')
api.add_resource(Infocrim, '/infocrim')
api.add_resource(Jucesp, '/jucesp')
api.add_resource(Siel, '/siel')
api.add_resource(Sivec, '/sivec')
api.add_resource(BolsaFamilia, '/bolsa-familia')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

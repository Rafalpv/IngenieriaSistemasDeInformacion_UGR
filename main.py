import os
from flask import Flask, render_template, redirect, url_for, request
from data.dieselGasolina import fecha

from classes.Combustible import Combustible
from classes.Gasolinera import Gasolinera
from classes.Entidad import Entidad
from classes.Ruta import Ruta

provincias_espana = [
    '', 'ALBACETE', 'ALICANTE', 'ALMERÍA', 'ARABA/ÁLAVA', 'ASTURIAS', 'ÁVILA', 'BADAJOZ', 'BARCELONA',
    'BURGOS', 'CÁCERES', 'CÁDIZ', 'CANTABRIA', 'CASTELLÓN / CASTELLÓ', 'CEUTA', 'CIUDAD REAL', 'CÓRDOBA', 'CUENCA',
    'GIRONA', 'GRANADA', 'GUADALAJARA', 'GIPUZKOA', 'HUELVA', 'HUESCA', 'ISLAS BALEARES', 'JAÉN',
    'CORUÑA (A)', 'RIOJA (LA)', 'PALMAS (LAS)', 'LEÓN', 'LLEIDA', 'LUGO', 'MADRID', 'MÁLAGA', 'MELILLA', 'MURCIA',
    'NAVARRA', 'ORENSE', 'PALENCIA', 'PONTEVEDRA', 'SALAMANCA', 'SANTA CRUZ DE TENERIFE', 'SEGOVIA',
    'SEVILLA', 'SORIA', 'TARRAGONA', 'TERUEL', 'TOLEDO', 'VALENCIA / VALÈNCIA', 'VALLADOLID', 'VIZCAYA',
    'ZAMORA', 'ZARAGOZA'
]

app = Flask(__name__)

@app.route("/")
def hello_world():
    return redirect(url_for("index"))


@app.route('/index.html')
def index():
    fechaPrecio = fecha()
    
    combustiblesEspaña = Combustible()
    preciosCombustiblesEspaña = combustiblesEspaña.getDatosCombustibles()
    
    entidades = Entidad()
    preciosEntidades = entidades.obtenerDatosEntidades()
    
    provincia = request.args.get('provincia')
    codPostal = request.args.get('codPostal')
    tipoCombustible = request.args.get('tipoCombustible')

    gasolinerasFiltrada = Gasolinera()    

    if (provincia == ''):
        gasolineras = gasolinerasFiltrada.getGasolinerasCodPostal(codPostal)
    else:
        gasolineras = gasolinerasFiltrada.getGasolinerasProvincia(provincia)

    return render_template('index.html', preciosCombustibles_web=preciosCombustiblesEspaña, fechaPrecio_web=fechaPrecio, preciosEntidades_web=preciosEntidades, provicinciasEspana_web=provincias_espana, gasolineras_web=gasolineras,tipoCombustible_web=tipoCombustible)


@app.route('/buscar_gasolineras', methods=['POST'])
def buscarGasolinerasProvincias():
    provincia = request.form['provincia']
    codPostal = request.form['codPostal']
    tipoCombustible = request.form['tipoCombustible']

    return redirect(url_for('index', provincia=provincia, codPostal=codPostal, tipoCombustible=tipoCombustible))


@app.route('/ciudades.html')
def ciudades():  
    ciudadPartida = request.args.get('ciudadPartida')
    ciudadDestino = request.args.get('ciudadDestino')

    ruta = Ruta(ciudadPartida,ciudadDestino)
    rutaCiudades = ruta.getRuta()
    infoRuta = ruta.informacionRuta()
    
    return render_template('ciudades.html', infoRuta_web=infoRuta, rutaCiudades_web=rutaCiudades)


@app.route("/procesar_formulario", methods=['POST'])
def formularioCiudades():
    
    ciudadPartida = request.form.get('ciudad_partida')
    ciudadDestino = request.form.get('ciudad_destino')
    
    return redirect(url_for('ciudades', ciudadPartida=ciudadPartida, ciudadDestino=ciudadDestino))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))

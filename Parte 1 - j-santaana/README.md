# La base de datos limpia está disponible dentro de la carpeta "Base de datos procesada"

# Instrucciones 

Para obtener la base de datos limpia

- Bajar la base de datos cruda desde [Aquí](https://archive.ics.uci.edu/dataset/374/appliances+energy+prediction)
- Colocar el archivo en la carpeta "base de datos cruda"
- Correr las celulas del jupyter de limpieza en orden
- La base de datos limpia debería estar en la carpeta "base de datos procesada"

# Descubrimientos

- La base de datos cuenta con 29 columnas y 19735 filas, no hay valores faltantes ni duplicados.
- La base de datos consiste en mediciones en intervalos de 10 minutos uno entre otro, y las condiciones climaticas locales
- La columna "Appliances" consiste en una columna target, con todas las demas siendo features, Cada Tx y RH_x corresponde a la temperatura y humedad en una habitación del hogar.
- To consiste en la temperatura afuera del hogar.

# Documentación de cambios 

- Cambiamos la columna "date" de su formato "object" a "DateTime"
- Eliminamos las columnas solicitadas rv1 y rv2
- Solo eliminamos valores anomalos correspondientes a valores negativos dentro del consumo o la humedad, ya que estos se deben a errores de mediciones, picos de consumo y momentos sin consumo electro son parte del dataset y del fenomeno a estudiar. Mientras que en los features, valores negativos o 0 en temperatura son posibles y esperables dependiendo del lugar donde se tomen las mediciones.




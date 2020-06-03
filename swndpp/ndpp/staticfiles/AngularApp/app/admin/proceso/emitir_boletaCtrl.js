(function(){
    "use strict";
    angular.module("DppApp")
        .controller("EmitirBoletaCtrl", ['$http', EmitirBoletaCtrl]);

    function EmitirBoletaCtrl($http){
        var self = this;

        self.afecto = true;

        self.items = [];
        self.items_impreso = [];

        self.total = 0;
        self.descuento = 6;

        self.numero = '0002-00';

        self.total_letra = '';

        self.departamento_boleta = "";
        self.fecha_boleta = "";

        self.items_selccionados = [];


        //inicializamos la lista de agentes
        $http.get("/api/departamento/")
          .then(function(response){
              self.departamentos = response.data;
          }
        );

        self.cargar_magazine = function(){
          self.descuento = 6;
          var d = new Date(self.fecha)
          var date = d.getDate() + "-" + (d.getMonth()+1) + "-" + d.getFullYear();
          //
          self.items_impreso = [];
          self.items = [];
          //
          $http.get("/api/emitir-boleta/"+date+"/"+self.rs+"/"+self.departamento+"/")
            .then(function(response){
                for (var i = 0; i < response.data.length; i++) {
                  if (response.data[i].impreso == true) {
                    self.items_impreso.push(response.data[i])
                  }
                  else {
                    self.items.push(response.data[i])
                  }
                }
                self.calcular_montos(self.items);
            }
          );
        }

        self.seleccionar_bloque = function(){
            console.log('...seleccionando bloque');
            if (self.items.length < 30) {
              for (var i = 0; i < self.items.length; i++) {
                self.items[i].emitido = true;
              }
            }
            else {
              for (var i = 0; i < 31; i++) {
                self.items[i].emitido = true;
              }
            }
            //calculamos monto
            self.aplicar_descuento();
            self.calcular_montos();
        }

        self.limpiar_bloque = function(){
            console.log('seleccionar_bloque');
            if (self.items.length < 30) {
              for (var i = 0; i < self.items.length; i++) {
                self.items[i].emitido = false;
              }
            }
            else {
              for (var i = 0; i < 31; i++) {
                self.items[i].emitido = false;
              }
            }
            //calculamos monto
            self.aplicar_descuento();
            self.calcular_montos();
        }

        self.calcular_montos = function(){
            self.total = 0;
            //primero verificamos el tipo de razon social
            for (var i = 0; i < self.items.length; i++) {
              if (self.items[i].emitido) {
                //sumamo monto
                self.total = parseFloat(self.total) + parseFloat(self.items[i].amount);
                self.total = self.total.toFixed(3);
              }
            }
        }

        //metodo para aplicar descuetno
        self.aplicar_descuento = function(){
          var dto = parseFloat(self.descuento);
          if (self.descuento == '') {
            dto = 0;
          }
          for (var i = 0; i < self.items.length; i++) {
            self.items[i].precio_sunat = parseFloat(self.items[i].precio_venta)-(dto/100)*(parseFloat(self.items[i].precio_venta));
            self.items[i].precio_sunat = self.items[i].precio_sunat.toFixed(3);
            self.items[i].amount = (self.items[i].precio_sunat*self.items[i].count).toFixed(3);
          }
          self.calcular_montos();
        }

        //validamos datos
        self.validar_datos = function(){
          if ((self.fecha) && (self.fecha_boleta) && (self.numero)) {
            return true;
          }
          else {
            return false;
          }
        }

        //funcion que genera la boleta
        self.generar_boleta = function(){
          console.log('funcion que genera boleta');
          if (self.validar_datos()) {
            //recuperamos fecha y departamento
            for (var i = 0; i < self.departamentos.length; i++) {
              if (self.departamento == self.departamentos[i].pk) {
                self.departamento_boleta = self.departamentos[i].name;
              }
            }
            //fecha
            var d = new Date(self.fecha_boleta)
            self.fecha_boleta_gen = d.getDate() + "-" + (d.getMonth()+1) + "-" + d.getFullYear();
            //primero cagregamos a una lista los selccionados
            console.log(self.departamento);
            self.items_selccionados = []
            for (var i = 0; i < self.items.length; i++) {
              if (self.items[i].emitido == true) {
                self.items_selccionados.push(self.items[i]);
              }
            }
            //calculamos total en letras
            self.total_letra = self.NumeroALetras(self.total);
          }
          else {
            console.log('los datos no son validos');
          }
        }

      // //metodo que guarda una boleta en la base de datos
      self.guardar_boleta = function(){
        console.log('... Emitiendo la boleta');
        //recuperamos las fechas
        var d1 = new Date(self.fecha)
        var date1 = d1.getFullYear() + "-" + (d1.getMonth()+1) + "-" + d1.getDate();
        //
        var d2 = new Date(self.fecha_boleta)
        var date2 = d2.getFullYear() + "-" + (d2.getMonth()+1) + "-" + d2.getDate();
        //generamos arreglo de boletas
        var items_boleta = [];
        for (var i = 0; i < self.items.length; i++) {
          console.log(date1);
          console.log(date2);
          if (self.items[i].emitido==true) {
            var item = {
              'detail_guide':self.items[i].pk,
              'total':self.total,
              'number':self.numero,
              'client':self.departamento_boleta,
              'date_emition':date2,
              'date_venta':date1,
              'count':self.items[i].count,
              'precio_venta':self.items[i].precio_venta,
              'precio_sunat':self.items[i].precio_sunat,
              'amount':self.items[i].amount,
              'afecto':self.afecto,
              'addressee':self.rs,
            };
            items_boleta.push(item);
          }
        }
        $http.post("/api/save/boleta/", items_boleta)
            .success(function(res){
              console.log(res);
              //$location.href
            })
            .error(function(res){
              console.log(res);
            });
      }

      //
      //
      //
      //   FUNCION PARA LEER UN NUMERO
      self.Unidades = function(num){

          switch(num)
          {
              case 1: return 'UN';
              case 2: return 'DOS';
              case 3: return 'TRES';
              case 4: return 'CUATRO';
              case 5: return 'CINCO';
              case 6: return 'SEIS';
              case 7: return 'SIETE';
              case 8: return 'OCHO';
              case 9: return 'NUEVE';
          }

          return '';
      }//Unidades()

      self.Decenas = function(num){

          var decena = Math.floor(num/10);
          var unidad = num - (decena * 10);

          switch(decena)
          {
              case 1:
                  switch(unidad)
                  {
                      case 0: return 'DIEZ';
                      case 1: return 'ONCE';
                      case 2: return 'DOCE';
                      case 3: return 'TRECE';
                      case 4: return 'CATORCE';
                      case 5: return 'QUINCE';
                      default: return 'DIECI' + self.Unidades(unidad);
                  }
              case 2:
                  switch(unidad)
                  {
                      case 0: return 'VEINTE';
                      default: return 'VEINTI' + self.Unidades(unidad);
                  }
              case 3: return self.DecenasY('TREINTA', unidad);
              case 4: return self.DecenasY('CUARENTA', unidad);
              case 5: return self.DecenasY('CINCUENTA', unidad);
              case 6: return self.DecenasY('SESENTA', unidad);
              case 7: return self.DecenasY('SETENTA', unidad);
              case 8: return self.DecenasY('OCHENTA', unidad);
              case 9: return self.DecenasY('NOVENTA', unidad);
              case 0: return self.Unidades(unidad);
          }
      }//Unidades()

      self.DecenasY = function(strSin, numUnidades) {
          if (numUnidades > 0)
          return strSin + ' Y ' + self.Unidades(numUnidades)

          return strSin;
      }//DecenasY()

      self.Centenas = function(num) {
          var centenas = Math.floor(num / 100);
          var decenas = num - (centenas * 100);

          switch(centenas)
          {
              case 1:
                  if (decenas > 0)
                      return 'CIENTO ' + self.Decenas(decenas);
                  return 'CIEN';
              case 2: return 'DOSCIENTOS ' + self.Decenas(decenas);
              case 3: return 'TRESCIENTOS ' + self.Decenas(decenas);
              case 4: return 'CUATROCIENTOS ' + self.Decenas(decenas);
              case 5: return 'QUINIENTOS ' + self.Decenas(decenas);
              case 6: return 'SEISCIENTOS ' + self.Decenas(decenas);
              case 7: return 'SETECIENTOS ' + self.Decenas(decenas);
              case 8: return 'OCHOCIENTOS ' + self.Decenas(decenas);
              case 9: return 'NOVECIENTOS ' + self.Decenas(decenas);
          }

          return self.Decenas(decenas);
      }//Centenas()

      self.Seccion = function(num, divisor, strSingular, strPlural) {
          var cientos = Math.floor(num / divisor)
          var resto = num - (cientos * divisor)

          var letras = '';

          if (cientos > 0)
              if (cientos > 1)
                  letras = self.Centenas(cientos) + ' '+ strPlural;
              else
                  letras = strSingular;

          if (resto > 0)
              letras += '';

          return letras;
      }//Seccion()

      self.Miles = function(num) {
          var divisor = 1000;
          var cientos = Math.floor(num / divisor)
          var resto = num - (cientos * divisor)

          var strMiles = self.Seccion(num, divisor, 'MIL', 'MIL');
          var strCentenas = self.Centenas(resto);

          if(strMiles == '')
              return strCentenas;

          return strMiles + ' ' + strCentenas;
      }//Miles()

      self.Millones = function(num) {
          var divisor = 1000000;
          var cientos = Math.floor(num / divisor)
          var resto = num - (cientos * divisor)

          var strMillones = self.Seccion(num, divisor, 'UN MILLON DE', 'MILLONES DE');
          var strMiles = self.Miles(resto);

          if(strMillones == '')
              return strMiles;

          return strMillones + ' ' + strMiles;
      }//Millones()

      self.NumeroALetras = function(num) {
          var data = {
              numero: num,
              enteros: Math.floor(num),
              centavos: (((Math.round(num * 100)) - (Math.floor(num) * 100))),
              letrasCentavos: '',
              letrasMonedaPlural: 'SOLES',
              letrasMonedaSingular: 'SOL',

              letrasMonedaCentavoPlural: 'CENTIMOS',
              letrasMonedaCentavoSingular: 'CENTIMO'
          };

          if (data.centavos > 0) {
              data.letrasCentavos = 'CON ' + String(data.centavos)+'/100 CENTIMOS';
              // (function (){
              //     if (data.centavos == 1)
              //         return self.Millones(data.centavos) + ' ' + data.letrasMonedaCentavoSingular;
              //     else
              //         return self.Millones(data.centavos) + ' ' + data.letrasMonedaCentavoPlural;
              //     })();
          };

          if(data.enteros == 0)
              return 'CERO ' + data.letrasMonedaPlural + ' ' + data.letrasCentavos;
          if (data.enteros == 1)
              return self.Millones(data.enteros) + ' ' + data.letrasMonedaSingular + ' ' + data.letrasCentavos;
          else
              return self.Millones(data.enteros) + ' ' + data.letrasMonedaPlural + ' ' + data.letrasCentavos;
      }
  }
}());

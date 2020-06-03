(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("ListBoletaCtrl", ['$http', ListBoletaCtrl]);

    function ListBoletaCtrl($http){
        var vm = this;

        vm.afecto = true;

        vm.total = 0;
        vm.descuento = 6;

        vm.cliente = "SINDICATO DE VENDEDORES Y DIARIOS";
        vm.seudonimo = "CUSCO";

        vm.numero = '0002-00';

        vm.total_letra = '';

        vm.total_boleta;

        vm.flat = false;

        vm.boletas = [];

        vm.json = [];


        //inicializamos la lista de agentes
        $http.get("/api/vendors")
          .then(function(response){
              vm.agentes = response.data;
              //creamos clinete falso
              var c = {
                'cod':'00000',
                'pk':0,
                'dni':'00000000',
                'name':'SINDICATO DE VENDEDORES Y DIARIOS',
                'type_vendor':'1',
                'seudonimo':'CUSCO',
                'line_credit':0,
                'disable':false,
              };
              vm.agentes.push(c);
              console.log(vm.agentes);
          }
        );

        vm.cargar_magazine = function(){
          vm.descuento = 6;
          var d = new Date(vm.fecha)
          var date = d.getDate() + "-" + (d.getMonth()+1) + "-" + d.getFullYear();
          //verificamos si existe rango
          var date2;
          if (vm.fecha2!=null) {
            var d2 = new Date(vm.fecha2)
            var date2 = d2.getDate() + "-" + (d2.getMonth()+1) + "-" + d2.getFullYear();
          }
          else {
            date2=date;
          }
          //
          console.log('rango de fechas:');
          console.log(date);
          console.log(date1);
          //
          $http.get("/api/boleta/items/"+date+"/"+date2+"/")
            .then(function(response){
                vm.items = response.data;
                vm.calcular_montos(vm.items);
            }
          );
        }

        //metodo que actualiza valor de sindicato
        vm.actualizar_cliente = function(){
            for (var i = 0; i < vm.agentes.length; i++) {
              if (vm.agentes[i].cod == vm.agente) {
                vm.cliente = vm.agentes[i].name;
                vm.seudonimo = vm.agentes[i].seudonimo;
              }
            }
        }

        vm.calcular_montos = function(lista){
            //primero verificamos el tipo de razon social
            if (vm.rs == '1') {
              vm.agente = "";
              var total = 0.00;
              for (var i = 0; i < lista.length; i++) {
                if ((lista[i].afecto == vm.afecto) && (lista[i].addressee == vm.rs)) {
                  total = total + parseFloat(lista[i].amount);
                }

              }
              vm.total = total.toFixed(2);
              vm.total_letra = vm.NumeroALetras(vm.total)
              vm.aplicar_descuento();
            }
            else {
              var total = 0.00;
              for (var i = 0; i < lista.length; i++) {
                if ((lista[i].afecto == vm.afecto) && (lista[i].addressee == vm.rs)&&(lista[i].vendor == vm.agente)) {
                  total = total + parseFloat(lista[i].amount);
                }

              }
              vm.total = total.toFixed(2);
              vm.total_letra = vm.NumeroALetras(vm.total)
              vm.aplicar_descuento();
            }
        }

        //metodo para aplicar descuetno
        vm.aplicar_descuento = function(){
          var dto = parseFloat(vm.descuento);
          if (vm.descuento == null) {
            dto = 0;
          }
          vm.total = 0;
          var total = 0.00;
          if (vm.rs == '1') {
            for (var i = 0; i < vm.items.length; i++) {
              if ((vm.items[i]!=null)&&(vm.items[i].emitido == true) && (vm.items[i].afecto == vm.afecto)&& (vm.items[i].addressee == vm.rs)) {
                  vm.items[i].precio_sunat = parseFloat(vm.items[i].precio_venta)-(dto/100)*(parseFloat(vm.items[i].precio_venta));
                  vm.items[i].precio_sunat = vm.items[i].precio_sunat.toFixed(3);
                  //ahora calculamos el monto total y los montos
                  vm.items[i].amount = vm.items[i].count*vm.items[i].precio_sunat;
                  vm.items[i].amount = vm.items[i].amount.toFixed(3);
                  total = total + parseFloat(vm.items[i].amount);
              }
            }
          }
          else {
            for (var i = 0; i < vm.items.length; i++) {
              if ((vm.items[i]!=null)&&(vm.items[i].emitido == true) && (vm.items[i].afecto == vm.afecto)&& (vm.items[i].addressee == vm.rs)&& (vm.items[i].vendor == vm.agente)) {
                  vm.items[i].precio_sunat = parseFloat(vm.items[i].precio_venta)-(dto/100)*(parseFloat(vm.items[i].precio_venta));
                  vm.items[i].precio_sunat = vm.items[i].precio_sunat.toFixed(3);
                  //ahora calculamos el monto total y los montos
                  vm.items[i].amount = vm.items[i].count*vm.items[i].precio_sunat;
                  vm.items[i].amount = vm.items[i].amount.toFixed(3);
                  total = total + parseFloat(vm.items[i].amount);
              }
            }
          }

          vm.total = total.toFixed(2);;
        }

        //metodo que actua con check
        vm.recalcular_monto = function(value, bool,pk){
            if (bool) {
              //calculamos el monto total
              vm.total = parseFloat(vm.total) + parseFloat(value);
              vm.total = vm.total.toFixed(2);
            }
            else {
              //calculamos el monto total
              vm.total = vm.total - parseFloat(value);
              vm.total = vm.total.toFixed(2);
            }

        }

        vm.quitar_item = function(){
          for (var i = 0; i < vm.items.length; i++) {
            if ((vm.items[i]!=null)&&(vm.items[i].emitido == false)) {
              delete vm.items[i];
            }
          }
        }


      //funcion para calcular monto total
      vm.calcular_total_boleta = function(lista){
        var total = 0;
        for (var i = 0; i < lista.length; i++) {
          total = parseFloat(total) + parseFloat(lista[i].amount);
        }
        return total.toFixed(2);
      }

      //funcion que imprime el pdf
      vm.generar_boleta = function(){

        vm.flat = true;

        var d = new Date(vm.fecha)
        var date_venta = d.getFullYear()+ "-" + (d.getMonth()+1) + "-" + d.getDate();

        var d2 = new Date(vm.fecha1)
        var date_emition = d2.getFullYear()+ "-" + (d2.getMonth()+1) + "-" + d2.getDate();

        var prods = [];
        //inicializamos variables
        vm.json = [];
        vm.boletas = [];
        vm.total_letra = "";
        vm.total_boleta = 0;

        //creamos objeto de impresion
        if (vm.rs == '1') {
          for (var i = 0; i < vm.items.length; i++) {
            console.log('---');
            if ((vm.items[i]!=null)&&(vm.items[i].emitido == true) && (vm.items[i].afecto == vm.afecto)&&(vm.items[i].addressee==vm.rs)&&(vm.items[i].impreso==false)) {
              console.log('*****');
              prods.push(vm.items[i])
            }
          }
        }
        else {
          for (var i = 0; i < vm.items.length; i++) {
            console.log('---');
            if ((vm.items[i]!=null)&&(vm.items[i].emitido == true) && (vm.items[i].afecto == vm.afecto)&&(vm.items[i].addressee==vm.rs)&&(vm.items[i].vendor==vm.agente)&&(vm.items[i].impreso==false)) {
            console.log('*****');
            prods.push(vm.items[i])
            }
          }
        }

        // si productos es de tamaño menor que 30
        if (prods.length < 30) {
          console.log('Menor que 30');
          //completamos prods a 30
          vm.total_boleta = vm.calcular_total_boleta(prods);

          vm.total_letra = vm.NumeroALetras(vm.total_boleta);
          //creamos json valido
          for (var i = 0; i < prods.length; i++) {
            //generamos imprimible
            vm.boletas.push(prods[i]);

            var itm = {
              'pk':prods[i].pk,
              'total':parseFloat(vm.total_boleta),
              'codigo':prods[i].codigo,
              'magazine':prods[i].magazine,
              'number':vm.numero,
              'client':vm.cliente,
              'vendor':vm.agente,
              'date_emition':date_emition,
              'date_venta':date_venta,
              'count':prods[i].count,
              'precio_venta':prods[i].precio_venta,
              'precio_sunat':prods[i].precio_sunat,
              'amount':prods[i].amount,
              'afecto':prods[i].afecto,
              'addressee':prods[i].addressee,
              'emitido':true,
              'impreso':true,
            }
            vm.json.push(itm);
          }

          //ahora completamos los productos a 30
          for (var i = 0; i < 30 - prods.length; i++) {
            var item = {
                'pk':'',
                'total':"",'codigo':"",'magazine':"",'number':"",
                'client':"",'date_emition':"",'date_venta':"",'count':"",
                'precio_venta':"",'precio_sunat':"",'amount':"",'afecto':"",
                'addressee':"",'vendor':"",'emitido':"",
            };
            vm.boletas.push(item);
          }

        }
        else {
          //generamos solo los primeros 30
          //creamos json valido
          for (var i = 0; i < 30; i++) {
            //generamos imprimible
            vm.boletas.push(prods[i]);

            var itm = {
              'pk':prods[i].pk,
              'total':0,
              'codigo':prods[i].codigo,
              'magazine':prods[i].magazine,
              'number':vm.numero,
              'client':vm.cliente,
              'vendor':vm.agente,
              'date_emition':date_emition,
              'date_venta':date_venta,
              'count':prods[i].count,
              'precio_venta':prods[i].precio_venta,
              'precio_sunat':prods[i].precio_sunat,
              'amount':prods[i].amount,
              'afecto':prods[i].afecto,
              'addressee':prods[i].addressee,
              'emitido':true,
              'impreso':true,
            }
            vm.json.push(itm);
          }
          vm.total_boleta = vm.calcular_total_boleta(vm.boletas);
          vm.total_letra = vm.NumeroALetras(vm.total_boleta);
          vm.json[0].total = parseFloat(vm.total_boleta);
        }
        //guardamos la data

      }


      //metodo que guarda una boleta en la base de datos
      vm.guardar_boleta = function(){
        //datos para guarda en tabla
        //enviamos los datos
        $http.post("/api/save/boleta/", vm.json)
            .success(function(res){
              console.log(res);
              //$location.href
            })
            .error(function(res){
              console.log(res);
            });
      }



      //   FUNCION PARA LEER UN NUMERO
      vm.Unidades = function(num){

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

      vm.Decenas = function(num){

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
                      default: return 'DIECI' + vm.Unidades(unidad);
                  }
              case 2:
                  switch(unidad)
                  {
                      case 0: return 'VEINTE';
                      default: return 'VEINTI' + vm.Unidades(unidad);
                  }
              case 3: return vm.DecenasY('TREINTA', unidad);
              case 4: return vm.DecenasY('CUARENTA', unidad);
              case 5: return vm.DecenasY('CINCUENTA', unidad);
              case 6: return vm.DecenasY('SESENTA', unidad);
              case 7: return vm.DecenasY('SETENTA', unidad);
              case 8: return vm.DecenasY('OCHENTA', unidad);
              case 9: return vm.DecenasY('NOVENTA', unidad);
              case 0: return vm.Unidades(unidad);
          }
      }//Unidades()

      vm.DecenasY = function(strSin, numUnidades) {
          if (numUnidades > 0)
          return strSin + ' Y ' + vm.Unidades(numUnidades)

          return strSin;
      }//DecenasY()

      vm.Centenas = function(num) {
          var centenas = Math.floor(num / 100);
          var decenas = num - (centenas * 100);

          switch(centenas)
          {
              case 1:
                  if (decenas > 0)
                      return 'CIENTO ' + vm.Decenas(decenas);
                  return 'CIEN';
              case 2: return 'DOSCIENTOS ' + vm.Decenas(decenas);
              case 3: return 'TRESCIENTOS ' + vm.Decenas(decenas);
              case 4: return 'CUATROCIENTOS ' + vm.Decenas(decenas);
              case 5: return 'QUINIENTOS ' + vm.Decenas(decenas);
              case 6: return 'SEISCIENTOS ' + vm.Decenas(decenas);
              case 7: return 'SETECIENTOS ' + vm.Decenas(decenas);
              case 8: return 'OCHOCIENTOS ' + vm.Decenas(decenas);
              case 9: return 'NOVECIENTOS ' + vm.Decenas(decenas);
          }

          return vm.Decenas(decenas);
      }//Centenas()

      vm.Seccion = function(num, divisor, strSingular, strPlural) {
          var cientos = Math.floor(num / divisor)
          var resto = num - (cientos * divisor)

          var letras = '';

          if (cientos > 0)
              if (cientos > 1)
                  letras = vm.Centenas(cientos) + ' '+ strPlural;
              else
                  letras = strSingular;

          if (resto > 0)
              letras += '';

          return letras;
      }//Seccion()

      vm.Miles = function(num) {
          var divisor = 1000;
          var cientos = Math.floor(num / divisor)
          var resto = num - (cientos * divisor)

          var strMiles = vm.Seccion(num, divisor, 'MIL', 'MIL');
          var strCentenas = vm.Centenas(resto);

          if(strMiles == '')
              return strCentenas;

          return strMiles + ' ' + strCentenas;
      }//Miles()

      vm.Millones = function(num) {
          var divisor = 1000000;
          var cientos = Math.floor(num / divisor)
          var resto = num - (cientos * divisor)

          var strMillones = vm.Seccion(num, divisor, 'UN MILLON DE', 'MILLONES DE');
          var strMiles = vm.Miles(resto);

          if(strMillones == '')
              return strMiles;

          return strMillones + ' ' + strMiles;
      }//Millones()

      vm.NumeroALetras = function(num) {
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
              //         return vm.Millones(data.centavos) + ' ' + data.letrasMonedaCentavoSingular;
              //     else
              //         return vm.Millones(data.centavos) + ' ' + data.letrasMonedaCentavoPlural;
              //     })();
          };

          if(data.enteros == 0)
              return 'CERO ' + data.letrasMonedaPlural + ' ' + data.letrasCentavos;
          if (data.enteros == 1)
              return vm.Millones(data.enteros) + ' ' + data.letrasMonedaSingular + ' ' + data.letrasCentavos;
          else
              return vm.Millones(data.enteros) + ' ' + data.letrasMonedaPlural + ' ' + data.letrasCentavos;
      }
  }
}());

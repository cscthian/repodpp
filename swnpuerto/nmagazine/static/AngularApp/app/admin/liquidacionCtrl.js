(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("LiquidacionCtrl",  ['$http', LiquidacionCtrl]);

    function LiquidacionCtrl($http){
      var vm = this;

      vm.error = false;
      vm.error2 = false;


      vm.liquidacion_dia = function(fecha){
        vm.error = false;
        var d = new Date(fecha)
        var date = d.getDate() + "-" + (d.getMonth()+1) + "-" + d.getFullYear();
        $http.get("/api/caja/liuidar/dia/"+date+'/')
          .then(function(response){
            vm.consulta = response.data;
            //generamos la impresion
            vm.imprimir_dia(vm.consulta,fecha);
          }
        )
        .catch(function(fallback) {
          vm.error = true;
          vm.mensjae = 'Datos Incorrectos';
        });
      }

      vm.imprimir_dia = function(consulta, date){
        //cambiamos el formato de fecha
        var meses = new Array ("Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre");
        var diasSemana = new Array("Domingo","Lunes","Martes","Miércoles","Jueves","Viernes","Sábado");
        var f=new Date(date);
        var fecha = diasSemana[f.getDay()] + ", " + f.getDate() + " de " + meses[f.getMonth()] + " de " + f.getFullYear();

        //generamos el arreglo contenido
        var mov = [];
        var suma_liquidaciondia = 0.00
        for (var i = 0; i < consulta.length; i++) {
          var row =[
              { text: consulta[i].pk + '  ' + consulta[i].canilla + '('+consulta[i].seudonimo+') - '+consulta[i].tipo, style: 'tableHeader', alignment: 'center' },
              { text: 'Devol', style: 'tableHeader', alignment: 'center' },
              { text: 'CantPago', style: 'tableHeader', alignment: 'center' },
              { text: 'MontoPago', style: 'tableHeader', alignment: 'center' }
          ];
          mov.push(row);
          //variable que suma los pagos
          var total = 0.00
          //iteramos los diarios
          for (var j = 0; j < consulta[i].movimientos.length; j++) {
            var t = new Date(consulta[i].movimientos[j].time)
            console.log(consulta[i].movimientos[j].devuelto);
            var time = t.getDate() + "/" + (t.getMonth() +1) + "/" + t.getFullYear() + "  hrs " + t.getHours() + ":" + t.getMinutes();
            var sub_row = [
              consulta[i].movimientos[j].pk_diario + ' '+consulta[i].movimientos[j].diario+' - '+time,
              consulta[i].movimientos[j].devuelto+'',
              consulta[i].movimientos[j].pagado+'',
              consulta[i].movimientos[j].monto,
            ]
            total = total + parseFloat(consulta[i].movimientos[j].monto);
            mov.push(sub_row);
          }
          mov.push(
            [ '', { colSpan: 3, rowSpan: 1, text: 'Total: S./ '+total.toFixed(3) }, '' ]
          );
          suma_liquidaciondia = suma_liquidaciondia + total;
        }
        var docDefinition = {
          content: [
            { text: 'DPP Reporte de Ventas Cobranzas y Devoluciones', style: 'subheader' },
            'Fecha: ' + fecha,
            'Monto Calculado: S/. '+suma_liquidaciondia.toFixed(3),
            {
                style: 'tableExample',
                color: '#444',
                table: {
                    widths: [ 300, 'auto', 'auto','auto'],
                    headerRows: 3,
                    // keepWithHeaderRows: 1,
                    body: mov,
                }
            },
          ],
          styles: {
        		header: {
        			fontSize: 18,
        			bold: true,
        			margin: [0, 0, 0, 10]
        		},
        		subheader: {
        			fontSize: 16,
        			bold: true,
        			margin: [0, 10, 0, 5]
        		},
        		tableExample: {
        			margin: [0, 5, 0, 15]
        		},
        		tableHeader: {
        			bold: true,
        			fontSize: 13,
        			color: 'black'
        		}
        	},
        	defaultStyle: {
        		// alignment: 'justify'
        	}
        };
        pdfMake.createPdf(docDefinition).open();
      }

      //funcion que consulta guias en rango de fechas
      vm.liquidacion_rango = function(fecha1, fecha2){
        vm.error2 = false;
        var d1 = new Date(fecha1)
        var d2 = new Date(fecha2)
        var date1 = d1.getDate() + "-" + (d1.getMonth()+1) + "-" + d1.getFullYear();
        var date2 = d2.getDate() + "-" + (d2.getMonth()+1) + "-" + d2.getFullYear();
        $http.get("/api/caja/liuidar/guia/"+date1+'/'+date2+'/')
          .then(function(response){
            console.log(response.data);
            vm.guias = response.data;
            //generamos la impresion
            vm.imprimir_rango(vm.guias,fecha1,fecha2);
          }
        )
        .catch(function(fallback) {
          vm.error2 = true;
          vm.mensaje2 = 'Datos Incorrectos';
        });
      }

      //funcion para imprimir reporte rango
      vm.imprimir_rango = function(consulta, date1, date2){
        //cambiamos el formato de fechas
        var meses = new Array ("Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre");
        var diasSemana = new Array("Domingo","Lunes","Martes","Miércoles","Jueves","Viernes","Sábado");
        var f=new Date(date1);
        var fecha1 = diasSemana[f.getDay()] + ", " + f.getDate() + " de " + meses[f.getMonth()] + " de " + f.getFullYear();

        var f2=new Date(date2);
        var fecha2 = diasSemana[f2.getDay()] + ", " + f2.getDate() + " de " + meses[f2.getMonth()] + " de " + f2.getFullYear();

        //generamos el arreglo contenido
        var liq = [];
        var head =[
            { text: 'Factura', style: 'tableHeader', alignment: 'center' },
            { text: 'Guia', style: 'tableHeader', alignment: 'center' },
            { text: 'Item', style: 'tableHeader', alignment: 'center' },
            { text: 'Fecha', style: 'tableHeader', alignment: 'center' },
            { text: 'Cantidad', style: 'tableHeader', alignment: 'center' },
            { text: 'Monto', style: 'tableHeader', alignment: 'center' },
            { text: 'Pre.U', style: 'tableHeader', alignment: 'center' },
            { text: 'DeVuelto', style: 'tableHeader', alignment: 'center' },
            { text: 'Vendido', style: 'tableHeader', alignment: 'center' },
            { text: 'Monto V', style: 'tableHeader', alignment: 'center' },
            { text: 'Proveedor', style: 'tableHeader', alignment: 'center' },
            { text: 'Total', style: 'tableHeader', alignment: 'center' },
        ];
        liq.push(head);
        var suma_liquidacionrango = 0.00;
        for (var i = 0; i < consulta.length; i++) {
          var total = vm.calcular_total(consulta[i].detalle);
          //agregamos el cuerpo
          for (var j = 0; j < consulta[i].detalle.length; j++) {
            var row = [
              consulta[i].number_invoce+'',
              consulta[i].number+'',
              consulta[i].detalle[j].magazine_day.substring(0,14)+'',
              consulta[i].date+'',
              consulta[i].detalle[j].count+'',
              (consulta[i].detalle[j].count*consulta[i].detalle[j].precio_guia).toFixed(3)+'',
              consulta[i].detalle[j].precio_guia+'',
              consulta[i].detalle[j].devuelto+'',
              consulta[i].detalle[j].vendido+'',
              (consulta[i].detalle[j].vendido*consulta[i].detalle[j].precio_guia).toFixed(3)+'',
              consulta[i].provider+'',
              { colSpan: 1, rowSpan:consulta[i].detalle.length, text: total.toFixed(3)+'', style: 'tableHeader', alignment: 'center'}
            ]
            liq.push(row);
          }

          liq.push([ '', '', '', '', '', '', '', '', '', '', '', '']);
          suma_liquidacionrango = suma_liquidacionrango + total;
        }
        var docDefinition = {
          pageOrientation: 'landscape',
          content: [
            { text: 'DPP Reporte Liquidacion de Guias', style: 'subheader' },
            { text:'Del: ' + fecha1 + ' / '+fecha2 },
            { text:'Monto Calculado: S/. '+suma_liquidacionrango.toFixed(3)},
            {
                style: 'tableExample',
                color: '#444',
                table: {
                    widths: [ 'auto', 'auto', 'auto', 'auto', 'auto', 'auto', 'auto', 'auto', 'auto', 'auto', 'auto', 'auto' ],
                    headerRows: 12,
                    // keepWithHeaderRows: 1,
                    body: liq,
                }
            },
          ],
          styles: {
        		header: {
        			fontSize: 10,
        			bold: true,
        			margin: [0, 5, 0, 10]
        		},
        		subheader: {
        			fontSize: 18,
        			bold: true,
        			margin: [0, 10, 0, 5]
        		},
        		tableExample: {
        			margin: [0, 5, 0, 15]
        		},
        		tableHeader: {
        			bold: true,
        			fontSize: 11,
        			color: 'black'
        		}
        	},
        	defaultStyle: {
        		// alignment: 'justify'
        	}
        };
        pdfMake.createPdf(docDefinition).open();
      }

      //funcion que suma valores
      vm.calcular_total = function(lista){
          var total = 0;
          for (var i = 0; i < lista.length; i++) {
            total = total + (lista[i].vendido*lista[i].precio_guia);
          }
          return total;
      }
    };
}())

(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("MargenCtrl",  ['$http', MargenCtrl]);

    function MargenCtrl($http){
      var vm = this;

      vm.error = false;

      //funcion que consulta guias en rango de fechas
    vm.margen_ganancia = function(fecha1, fecha2){
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
        //[ { rowSpan: 3, text: 'rowSpan set to 3\nLorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor' }, 'Sample value 2', 'Sample value 3' ],
        var head =[
            { text: 'Guia', style: 'tableHeader', alignment: 'center' },
            { text: 'Item', style: 'tableHeader', alignment: 'center' },
            { text: 'Fecha', style: 'tableHeader', alignment: 'center' },
            { text: 'Cantidad', style: 'tableHeader', alignment: 'center' },
            { text: 'Pre.V', style: 'tableHeader', alignment: 'center' },
            { text: 'Pre.G', style: 'tableHeader', alignment: 'center' },
            { text: 'Devuelto', style: 'tableHeader', alignment: 'center' },
            { text: 'Vendido', style: 'tableHeader', alignment: 'center' },
            { text: 'Monto V', style: 'tableHeader', alignment: 'center' },
            { text: 'Total', style: 'tableHeader', alignment: 'center' },
        ];
        liq.push(head);
        var suma_liquidacionrango = 0.00
        for (var i = 0; i < consulta.length; i++) {
          var total = 0.00
          //agregamos el cuerpo
          for (var j = 0; j < consulta[i].detalle.length; j++) {
            total = total + (consulta[i].detalle[j].vendido*(consulta[i].detalle[j].precio_venta-consulta[i].detalle[j].precio_guia));
            var row = [
              consulta[i].number+'',
              consulta[i].detalle[j].magazine_day.substring(0,14)+'',
              consulta[i].date+'',
              consulta[i].detalle[j].count+'',
              consulta[i].detalle[j].precio_venta+'',
              consulta[i].detalle[j].precio_guia+'',
              consulta[i].detalle[j].devuelto+'',
              consulta[i].detalle[j].vendido+'',
              (consulta[i].detalle[j].vendido*(consulta[i].detalle[j].precio_venta - consulta[i].detalle[j].precio_guia )).toFixed(3)+'',
              { colSpan: 1, rowSpan:consulta[i].detalle.length, text: total.toFixed(3)+'', style: 'tableHeader', alignment: 'center'}
            ]
            liq.push(row);
          }

          liq.push([ '', '', '', '', '', '', '', '', '', '']);
          suma_liquidacionrango = suma_liquidacionrango + total;
        }
        var docDefinition = {
          // by default we use portrait, you can change it to landscape if you wish
          content: [
            { text: 'DPP Reporte Liquidacion de Guias', style: 'subheader' },
            'del: ' + fecha1 + ' / '+fecha2,
            'Monto Calculado: S/. '+suma_liquidacionrango.toFixed(3),
            {
                style: 'tableExample',
                color: '#444',
                table: {
                    widths: [ 'auto', 'auto', 'auto', 'auto', 'auto', 'auto', 'auto', 'auto', 'auto', 'auto' ],
                    headerRows: 10,
                    // keepWithHeaderRows: 1,
                    body: liq,
                }
            },
          ],
          styles: {
        		header: {
        			fontSize: 10,
        			bold: true,
        			margin: [0, 0, 0, 10]
        		},
        		subheader: {
        			fontSize: 10,
        			bold: true,
        			margin: [0, 10, 0, 5]
        		},
        		tableExample: {
        			margin: [0, 5, 0, 15]
        		},
        		tableHeader: {
        			bold: true,
        			fontSize: 8,
        			color: 'black'
        		}
        	},
        	defaultStyle: {
        		// alignment: 'justify'
        	}
        };
        pdfMake.createPdf(docDefinition).open();
      }


      //funcion que grafica reporte
      vm.cargar_datos = function(){
        $http.get("/api/ventas/cierre/ingreso-neto/")
          .then(function(response){
              vm.myDataSource.data  = response.data;
              console.log('entro');
          }
        );
      }
      vm.myDataSource = {
        chart: {
            caption: "Reporte Ingresos",
            subCaption: "Top 5 ultimos meses",
            "xAxisName": "Mes",
            "yAxisName": "Ingresos (Soles)",
            "numberPrefix": "S/.",
          },
      };

    };
}())

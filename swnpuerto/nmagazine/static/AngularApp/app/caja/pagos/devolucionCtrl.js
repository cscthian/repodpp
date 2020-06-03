(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("DevolucionCtrl",  ['$http','uiGridConstants', DevolucionCtrl]);

    //MagazineCtrl.$inject = ["NgTableParams"];

    function DevolucionCtrl($http,uiGridConstants){
      var vm = this;

      var date_aux = new Date()
      var date_emision = date_aux.getDate() + "/" + (date_aux.getMonth()+1) + "/" + date_aux.getFullYear();

      vm.total = 0.000;

      vm.gridOptions = {
        infiniteScrollRowsFromEnd: 40,
        infiniteScrollUp: true,
        columnDefs : [
          {
            name: 'date',
            enableColumnMenu: false,
            displayName: 'Fecha Entre',
            enableCellEdit: false,
            width: 100
          },
          {
            name: 'magazine',
            displayName: 'Nombre',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false
          },
          {
            name: 'tipo',
            displayName: 'Tipo',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false
          },
          {
            name: 'devuelto',
            displayName: 'Devuelto',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            type: 'number',
          },
        ],
        //personalizamos el pdf
        enableGridMenu: false,
        enableSelectAll: false,
        exporterMenuCsv: false,
        exporterMenuPdf: false,
        exporterPdfDefaultStyle: {fontSize: 9},
        exporterPdfTableStyle: {margin: [10, 30, 10, 30]},
        exporterPdfTableHeaderStyle: {fontSize: 10, bold: true, italics: true, color: 'red'},
        exporterPdfHeader: { text: "Informe Devoluciones ("+date_emision+")", style: 'headerStyle' },
        exporterPdfFooter: function ( currentPage, pageCount ) {
          return { text: currentPage.toString() + ' de ' + pageCount.toString(), style: 'footerStyle' };
        },
        exporterPdfCustomFormatter: function ( docDefinition ) {
          docDefinition.styles.headerStyle = { fontSize: 13, bold: true, margin: [200, 20, 10, 10] };
          docDefinition.styles.footerStyle = { fontSize: 10, bold: true };
          return docDefinition;
        },
        exporterPdfOrientation: 'portrait',
        exporterPdfPageSize: 'LETTER',
        exporterPdfMaxGridWidth: 500,
      };

      //cargamos la lista de movimientos
      vm.cargar_devolucion_caja = function(){
        $http.get("/api/pagos/caja/cudrar/liquidacion/")
          .then(function(response){
              vm.gridOptions.data = response.data;
          }
        )
        .catch(function(fallback) {
          console.log('nose pudo conectar');
        });
      }

      vm.gridOptions.enableCellEditOnFocus = true;
      vm.currentFocused = "";

      vm.gridOptions.onRegisterApi = function(gridApi){
        vm.gridApi = gridApi;
      };

      vm.exportar_pdf = function(){
        //cambiamos el formato de fecha
        var meses = new Array ("Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre");
        var diasSemana = new Array("Domingo","Lunes","Martes","Miércoles","Jueves","Viernes","Sábado");
        var f=new Date(date_aux);
        var fecha = diasSemana[f.getDay()] + ", " + f.getDate() + " de " + meses[f.getMonth()] + " de " + f.getFullYear();

        //generamos el arreglo contenido
        var filas = [];
        var total = 0.00

        var head =[
            { text: 'Fecha', style: 'tableHeader' },
            { text: 'Diario/Producto', style: 'tableHeader' },
            { text: 'Tipo', style: 'tableHeader' },
            { text: 'Devuelto', style: 'tableHeader' },
        ];
        filas.push(head);


        for (var i = 0; i < vm.gridOptions.data.length; i++) {
            var row = [
                vm.gridOptions.data[i].date,
                vm.gridOptions.data[i].magazine,
                vm.gridOptions.data[i].tipo,
                vm.gridOptions.data[i].devuelto+''
            ];
            filas.push(row);
        }
        console.log('filas: '+filas);
        var docDefinition = {
          content: [
            { text: 'DPP Reporte Devoluciones del Dia', style: 'subheader' },
            'Fecha: ' + fecha,

            {
    						style: 'tableExample',
    						table: {
    								headerRows: 1,
    								body: filas,
    						},
    						layout: 'lightHorizontalLines'
    				},
            { text: '.',style: 'subheader2'},
            { text: '.',style: 'subheader2'},
            { text: '.',style: 'subheader2'},
            {
                columns: [
                    { text:  'Personal Almacen',decoration: 'overline'},
                    { text:  'Personal Caja', decoration: 'overline'},
                    { text:  'Administracion', decoration: 'overline'}
                ]
            }
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
            subheader2: {
        			fontSize: 2,
        			bold: false,
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
      vm.exportarExcel = function(){
          vm.gridApi.exporter.csvExport('all', 'selected');
      }

    }
}())

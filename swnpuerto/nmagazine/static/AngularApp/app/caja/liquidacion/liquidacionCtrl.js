(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("LiquidacionCtrl",  ['$http', LiquidacionCtrl]);

    function LiquidacionCtrl($http){
      var vm = this;

      var total = 0;

      vm.gridOptions = {
        columnDefs : [
          {
            name: 'factura',
            enableColumnMenu: false,
            displayName: 'Factura',
            enableCellEdit: false,
            width: 80
          },
          {
            name: 'guide',
            displayName: 'N° Guia',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 90
          },
          {
            name: 'magazine',
            displayName: 'Item',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 140
          },
          {
            name: 'date',
            displayName: 'Fecha Rec.',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 90
          },
          {
            name: 'count',
            displayName: 'Can.Rec',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            type: 'number',
            width: 50
          },
          {
            name: 'amount_total',
            displayName: 'Total',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            type: 'number',
            width: 60
          },
          {
            name: 'precio_unitario',
            displayName: 'Precio U',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            type: 'number',
            width: 60
          },
          {
            name: 'devuelto',
            displayName: 'Devol',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            type: 'number',
            width: 50
          },
          {
            name: 'vendido',
            displayName: 'Vend',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            type: 'number',
            width: 50
          },
          {
            name: 'amount_vendido',
            displayName: 'Total Ven.',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            type: 'number',
            width: 60
          },
          {
            name: 'provider',
            displayName: 'Proveedor',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 60
          },
          {
            name: 'amount',
            displayName: 'Monto Cal.',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 70
          },
        ],
        //personalizamos el pdf
        infiniteScrollRowsFromEnd: 10,
        enableHorizontalScrollbar: true,
        infiniteScrollUp: true,
        enableGridMenu: true,
        exporterPdfDefaultStyle: {fontSize: 9},
        exporterPdfTableStyle: {margin: [10, 30, 10, 30]},
        exporterPdfTableHeaderStyle: {fontSize: 10, bold: true, italics: true, color: 'red'},
        exporterPdfHeader: { text: "Liquidacion por Proveedor DPP", style: 'headerStyle' },
        exporterPdfFooter: function ( currentPage, pageCount ) {
          return { text: currentPage.toString() + ' de ' + pageCount.toString(), style: 'footerStyle' };
        },
        exporterPdfCustomFormatter: function ( docDefinition ) {
          docDefinition.styles.headerStyle = { fontSize: 13, bold: true, margin: [20, 20, 10, 10] };
          docDefinition.styles.footerStyle = { fontSize: 10, bold: true };
          return docDefinition;
        },
        exporterPdfOrientation: 'landscape',
        exporterPdfPageSize: 'LETTER',
        exporterPdfMaxGridWidth: 600,

        onRegisterApi: function(gridApi) {
          vm.gridApi = gridApi;
        }
      };

      //inicializamos la lista de proveedores
      $http.get("/api/provider")
        .then(function(response){
            vm.providers = response.data;
        }
      );

      //funcion que consulta guias en rango de fechas
      vm.liquidacion_rango = function(fecha1, fecha2){
        var d1 = new Date(fecha1)
        var d2 = new Date(fecha2)
        var date1 = d1.getDate() + "-" + (d1.getMonth()+1) + "-" + d1.getFullYear();
        var date2 = d2.getDate() + "-" + (d2.getMonth()+1) + "-" + d2.getFullYear();
        $http.get("/api/caja/liuidar/guia/"+date1+'/'+date2+'/'+vm.provider+'/')
          .then(function(response){
            console.log(response.data);
            vm.gridOptions.data = response.data;
            //generamos la impresion
          }
        )
        .catch(function(fallback) {
          console.log('error');
        });
      }


      //funcion que suma valores
      vm.calcular_total = function(){
          total = 0;
          for (var i = 0; i < vm.gridOptions.data.length; i++) {
            if (vm.gridOptions.data[i].amount != ' ') {
              console.log('---'+vm.gridOptions.data[i].amount);
              total = total + parseFloat(vm.gridOptions.data[i].amount);
            }

          }
          return total;
      }
      vm.exportar_pdf = function(){
        var d1 = new Date(vm.fecha1)
        var d2 = new Date(vm.fecha2)
        var date1 = d1.getDate() + "/" + (d1.getMonth()+1) + "/" + d1.getFullYear();
        var date2 = d2.getDate() + "/" + (d2.getMonth()+1) + "/" + d2.getFullYear();

        vm.calcular_total();

        vm.gridOptions.exporterPdfHeader.text = "Liquidacion por Proveedor DPP: "+vm.provider+" "+" de ["+date1+"] - ["+date2+"]"+" Total: S/."+total.toFixed(3);
        vm.gridOptions.exporterPdfHeader.style = 'headerStyle'
        vm.gridApi.exporter.pdfExport('all', 'selected');
      }
      vm.exportarExcel = function(){
        vm.gridApi.exporter.csvExport('all', 'selected');
      }
    };
}())

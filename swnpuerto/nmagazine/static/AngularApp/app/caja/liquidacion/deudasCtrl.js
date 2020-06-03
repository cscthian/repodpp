(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("DeudasCtrl",  ['$http', DeudasCtrl]);

    function DeudasCtrl($http){
      var vm = this;

      var total = 0;

      vm.gridOptions = {
        columnDefs : [
          {
            name: 'vendor',
            displayName: 'Nombres Apellidos',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 200
          },
          {
            name: 'magazine',
            displayName: 'Item',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 130
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
            name: 'entregado',
            displayName: 'Entre',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            type: 'number',
          },
          {
            name: 'devuelto',
            displayName: 'Devol',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            type: 'number',
          },
          {
            name: 'pagado',
            displayName: 'Paga',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            type: 'number',
          },
          {
            name: 'debe',
            displayName: 'Debe',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            type: 'number',
          },
          {
            name: 'precio_unitario',
            displayName: 'Prec.U',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            type: 'number',
          },
          {
            name: 'monto_deuda',
            displayName: 'M. Deuda',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            type: 'number',
          },
          {
            name: 'monto_pagado',
            displayName: 'M. Pagado',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
          },
          {
            name: 'amount',
            displayName: 'Total',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
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
        exporterPdfHeader: { text: "Movimientos de Caja DPP", style: 'headerStyle' },
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

      //funcion que consulta guias en rango de fechas
      vm.generar_deudas = function(){
        var d1 = new Date(vm.fecha)
        var date1 = d1.getDate() + "-" + (d1.getMonth()+1) + "-" + d1.getFullYear();
        $http.get("/api/caja/liuidar/deudas/"+date1+'/')
          .then(function(response){
            vm.gridOptions.data = response.data;
            for (var i = 0; i < vm.gridOptions.data.length; i++) {
              vm.gridOptions.data[i].magazine = vm.gridOptions.data[i].magazine.slice(0,14);
            }
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
        var d1 = new Date(vm.fecha)
        var date1 = d1.getDate() + "/" + (d1.getMonth()+1) + "/" + d1.getFullYear();

        vm.calcular_total();

        vm.gridOptions.exporterPdfHeader.text = "Movimientos de Caja DPP: "+" de ["+date1+"]"+" Total: S/."+total.toFixed(3);
        vm.gridOptions.exporterPdfHeader.style = 'headerStyle'
        vm.gridApi.exporter.pdfExport('all', 'selected');
      }
      vm.exportarExcel = function(){
        vm.gridApi.exporter.csvExport('all', 'selected');
      }
    };
}())

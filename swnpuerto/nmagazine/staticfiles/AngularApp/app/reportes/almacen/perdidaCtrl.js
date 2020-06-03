(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("PerididaCtrl",  ['$http','uiGridConstants','ngToast', PerididaCtrl]);

    //MagazineCtrl.$inject = ["NgTableParams"];

    function PerididaCtrl($http,uiGridConstants,ngToast){
      var vm = this;

      vm.total = 0.000;

      vm.gridOptions = {
        infiniteScrollRowsFromEnd: 40,
        infiniteScrollUp: true,
        columnDefs : [
          {
            name: 'pk',
            enableColumnMenu: false,
            displayName: 'Codigo',
            enableCellEdit: false,
            width: 100
          },
          {
            name: 'name',
            displayName: 'Nombre',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false
          },
          {
            name: 'perdido',
            displayName: 'Perdido',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            type: 'number',
          },
          {
            name: 'monto',
            displayName: 'Monto(S/.)',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            type: 'number',
          },
        ],
        //personalizamos el pdf
        enableGridMenu: true,
        enableSelectAll: false,
        exporterMenuCsv: false,
        exporterMenuPdf: false,
        exporterPdfDefaultStyle: {fontSize: 9},
        exporterPdfTableStyle: {margin: [10, 30, 30, 30]},
        exporterPdfTableHeaderStyle: {fontSize: 10, bold: true, italics: true, color: 'red'},
        exporterPdfHeader: { text: "Perdida de Producto/diario", style: 'headerStyle' },
        exporterPdfFooter: function ( currentPage, pageCount ) {
          return { text: currentPage.toString() + ' de ' + pageCount.toString(), style: 'footerStyle' };
        },
        exporterPdfCustomFormatter: function ( docDefinition ) {
          docDefinition.styles.headerStyle = { fontSize: 15, bold: true, margin: [250, 0, 20, 0] };
          docDefinition.styles.footerStyle = { fontSize: 10, bold: true };
          return docDefinition;
        },
        exporterPdfOrientation: 'portrait',
        exporterPdfPageSize: 'LETTER',
        exporterPdfMaxGridWidth: 500,
      };

      //cargamos la lista de canillas
      vm.generar_ranking = function(fecha1, fecha2){
        var d1 = new Date(fecha1)
        var d2 = new Date(fecha2)
        var date1 = d1.getDate() + "-" + (d1.getMonth()+1) + "-" + d1.getFullYear();
        var date2 = d2.getDate() + "-" + (d2.getMonth()+1) + "-" + d2.getFullYear();
        $http.get("/api/reportes/diario/"+date1+'/'+date2+'/'+'0001')
          .then(function(response){
              vm.gridOptions.data = response.data;
              var total = 0.00;
              for (var i = 0; i < vm.gridOptions.data.length; i++) {
                  total = total + parseFloat(vm.gridOptions.data[i].monto);
              }
              vm.total = total.toFixed(3);
          }
        );

        //claulamos el tototal

      }
      vm.gridOptions.enableCellEditOnFocus = true;
      vm.currentFocused = "";

      vm.gridOptions.onRegisterApi = function(gridApi){
        vm.gridApi = gridApi;
      };

      vm.exportar_pdf = function(){
          vm.gridApi.exporter.pdfExport('all', 'selected');
      }
      vm.exportarExcel = function(){
          vm.gridApi.exporter.csvExport('all', 'selected');
      }

    }
}())

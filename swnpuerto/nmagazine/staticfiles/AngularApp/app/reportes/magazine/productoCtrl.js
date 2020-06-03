(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("ProductCtrl",  ['$http','uiGridConstants','ngToast', ProductCtrl]);

    //MagazineCtrl.$inject = ["NgTableParams"];

    function ProductCtrl($http,uiGridConstants,ngToast){
      var vm = this;

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
            name: 'vendido',
            displayName: 'Vendido',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false
          },
          {
            name: 'devuelto',
            displayName: 'Devuelto',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false
          },
          {
            name: 'perdido',
            displayName: 'Perdido',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false
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
        exporterPdfHeader: { text: "DPP: Ranking Productos", style: 'headerStyle' },
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
        $http.get("/api/reportes/diario/"+date1+'/'+date2+'/'+'1')
          .then(function(response){
              vm.gridOptions.data = response.data;
          }
        );
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

(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("TopeCtrl",  ['$http','uiGridConstants','ngToast', TopeCtrl]);

    //MagazineCtrl.$inject = ["NgTableParams"];

    function TopeCtrl($http,uiGridConstants,ngToast){
      var vm = this;

      vm.gridOptions = {
        infiniteScrollRowsFromEnd: 5,
        infiniteScrollUp: true,
        columnDefs : [
          {
            name: 'cod',
            enableColumnMenu: false,
            sort: {
              direction: uiGridConstants.ASC,
              priority: 0
            },
            displayName: 'Codigo',
            type: 'number',
            enableCellEdit: false,
            width: 100
          },
          {
            name: 'name',
            displayName: 'Nombre',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 300
          },
          {
            name: 'tipo',
            displayName: 'Tipo',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false
          },
          {
            name: 'tope',
            displayName: 'Tope Credito(S/.)',
            type: 'number',
            enableColumnMenu: false,
            enableCellEdit: false,
            type: 'number',
            enableCellEditOnFocus:false
          },
          {
            name: 'deuda',
            displayName: 'Deuda(S/.)',
            type: 'number',
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
        exporterPdfHeader: { text: "DPP:  Ranking Canillas", style: 'headerStyle' },
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
      vm.generar_ranking = function(){
        $http.get("/api/reportes/canillas/lista/")
          .then(function(response){
              //lamamos funcion que calcula tope
              vm.calcular_tope(response.data);
          }
        );
      }
      vm.gridOptions.enableCellEditOnFocus = true;
      vm.currentFocused = "";

      vm.gridOptions.onRegisterApi = function(gridApi){
        vm.gridApi = gridApi;
      };

      //funcion para calculartope de credito
      vm.calcular_tope = function(lista){
          for (var i = 0; i < lista.length; i++) {
            if (lista[i].deuda < (lista[i].tope-20)) {
                delete lista[i];
            }
          }
          vm.gridOptions.data = lista;
      }

      vm.exportar_pdf = function(){
          vm.gridApi.exporter.pdfExport('all', 'selected');
      }
      vm.exportarExcel = function(){
          vm.gridApi.exporter.csvExport('all', 'selected');
      }

    }
}())

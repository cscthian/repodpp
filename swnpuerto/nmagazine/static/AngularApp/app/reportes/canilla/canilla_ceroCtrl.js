(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("CeroCtrl",  ['$http','uiGridConstants','ngToast', CeroCtrl]);

    //MagazineCtrl.$inject = ["NgTableParams"];

    function CeroCtrl($http,uiGridConstants,ngToast){
      var vm = this;

      vm.gridOptions = {
        enableFiltering: true,
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
            name: 'lunes',
            displayName: 'L',
            type: 'number',
            enableColumnMenu: false,
            enableCellEdit: false,
            type: 'number',
            enableCellEditOnFocus:false
          },
          {
            name: 'martes',
            displayName: 'M',
            type: 'number',
            enableColumnMenu: false,
            enableCellEdit: false,
            type: 'number',
            enableCellEditOnFocus:false
          },
          {
            name: 'miercoles',
            displayName: 'Mi',
            type: 'number',
            enableColumnMenu: false,
            enableCellEdit: false,
            type: 'number',
            enableCellEditOnFocus:false
          },
          {
            name: 'jueves',
            displayName: 'J',
            type: 'number',
            enableColumnMenu: false,
            enableCellEdit: false,
            type: 'number',
            enableCellEditOnFocus:false
          },
          {
            name: 'viernes',
            displayName: 'V',
            type: 'number',
            enableColumnMenu: false,
            enableCellEdit: false,
            type: 'number',
            enableCellEditOnFocus:false
          },
          {
            name: 'sabado',
            displayName: 'S',
            type: 'number',
            enableColumnMenu: false,
            enableCellEdit: false,
            type: 'number',
            enableCellEditOnFocus:false
          },
          {
            name: 'domingo',
            displayName: 'D',
            type: 'number',
            enableColumnMenu: false,
            enableCellEdit: false,
            type: 'number',
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
        exporterPdfOrientation: 'landscape',
        exporterPdfPageSize: 'LETTER',
        exporterPdfMaxGridWidth: 500,
      };

      //cargamos la lista de canillas
      $http.get("/api/magazin")
        .then(function(response){
            vm.diarios = response.data;
        }
      );

      vm.generar_ranking = function(diario){
        $http.get("/api/reportes/canilla/cero/"+diario+"/")
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

(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("RankincanillaCtrl",  ['$http','uiGridConstants','ngToast', RankincanillaCtrl]);

    //MagazineCtrl.$inject = ["NgTableParams"];

    function RankincanillaCtrl($http,uiGridConstants,ngToast){
      var vm = this;

      vm.gridOptions = {
        infiniteScrollRowsFromEnd: 5,
        infiniteScrollUp: true,
        columnDefs : [
          {
            name: 'num',
            enableColumnMenu: false,
            displayName: 'N°',
            type: 'number',
            enableCellEdit: false,
            width: 50
          },
          {
            name: 'cod',
            enableColumnMenu: false,
            displayName: 'Codigo',
            type: 'number',
            enableCellEdit: false,
            width: 80
          },
          {
            name: 'name',
            displayName: 'Nombre',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 250
          },
          {
            name: 'entregado',
            displayName: 'Entregado',
            type: 'number',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 80
          },
          {
            name: 'vendido',
            displayName: 'Vendido',
            type: 'number',
            cellClass:'gray',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 80
          },
          {
            name: 'devuelto',
            displayName: 'Devuelto',
            type: 'number',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 80
          },
        ],
        //personalizamos el pdf
        enableGridMenu: true,
        enableSelectAll: false,
        exporterMenuCsv: false,
        exporterMenuPdf: false,
        exporterPdfDefaultStyle: {fontSize: 9},
        exporterPdfTableStyle: {margin: [30, 15, 0, 0]},
        exporterPdfTableHeaderStyle: {fontSize: 10, bold: true, italics: true, color: 'red'},
        exporterPdfHeader: { text: "DPP:  Ranking Canillas (Mejores Vendedores)", style: 'headerStyle' },
        exporterPdfFooter: function ( currentPage, pageCount ) {
          return { text: currentPage.toString() + ' de ' + pageCount.toString(), style: 'footerStyle' };
        },
        exporterPdfCustomFormatter: function ( docDefinition ) {
          docDefinition.styles.headerStyle = { fontSize: 15, bold: true, margin: [60, 20, 20, 0] };
          docDefinition.styles.footerStyle = { fontSize: 10, bold: true };
          return docDefinition;
        },
        exporterPdfOrientation: 'portrait',
        exporterPdfPageSize: 'LETTER',
        exporterPdfMaxGridWidth: 450,
      };

      //cargamos la lista de diarios
      $http.get("/api/magazin")
        .then(function(response){
            vm.diarios = response.data;
        }
      );

      //cargamos la lista de canillas
      vm.generar_ranking = function(magazine){
        $http.get("/api/reportes/canillas/lista/"+magazine+"/")
          .then(function(response){
              vm.gridOptions.data = response.data;
              //asigamos un indice
              for (var i = 0; i < vm.gridOptions.data.length; i++) {
                vm.gridOptions.data[i].num = i +1;
              }
          }
        );
      }
      vm.gridOptions.enableCellEditOnFocus = true;
      vm.currentFocused = "";

      vm.gridOptions.onRegisterApi = function(gridApi){
        vm.gridApi = gridApi;
      };

      vm.exportar_pdf = function(){
          //recuperaos el diario
          var diario;
          for (var i = 0; i < vm.diarios.length; i++) {
            if (vm.diarios[i].pk == vm.magazine) {
              diario = vm.diarios[i].name;
            }
          }
          vm.gridOptions.exporterPdfHeader.text = "Reporte de Mejores Vendedores DPP: "+" Diario("+diario+")";
          vm.gridOptions.exporterPdfHeader.style = 'headerStyle'
          vm.gridApi.exporter.pdfExport('all', 'selected');
      }
      vm.exportarExcel = function(){
          vm.gridApi.exporter.csvExport('all', 'selected');
      }

    }
}())

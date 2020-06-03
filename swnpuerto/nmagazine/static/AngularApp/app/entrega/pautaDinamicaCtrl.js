(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("PautaDinamicaCtrl",  ['$http','uiGridConstants','ngToast', PautaDinamicaCtrl]);

    function PautaDinamicaCtrl($http,uiGridConstants,ngToast){
      var vm = this;

      vm.canillas = {};

      //inicialiamos nuestra tabla
      vm.columns = [
        { field: 'Codigo',enableCellEdit: false,enableColumnMenu: false,type: 'number' },
        { field: 'Nombres', enableCellEdit: false,enableColumnMenu: false}
      ];
      vm.gridOptions = {
        infiniteScrollRowsFromEnd: 40,
        infiniteScrollUp: true,

        enableSorting: true,
        columnDefs: vm.columns,
        enableGridMenu: true,
        enableSelectAll: false,
        exporterMenuCsv: false,
        exporterMenuPdf: false,
        exporterPdfDefaultStyle: {fontSize: 9},
        exporterPdfTableStyle: {margin: [-15, 10, 10, 10]},
        exporterPdfTableHeaderStyle: {fontSize: 10, bold: true, italics: true, color: 'red'},
        exporterPdfHeader: { text: "DPP Pauta de Entrega", style: 'headerStyle' },
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

        onRegisterApi: function(gridApi) {
          vm.gridApi = gridApi;
        }
      };
      //metodo para inicializar la tabla dinamica
      vm.cargar_tabla = function(){
        $http.get("/api/pautas/dinamica/generar/"+vm.dia+"/")
          .then(function(response){
              vm.canillas = response.data;
              if (vm.canillas.length > 0) {

                var diarios = vm.canillas[0].product;
                vm.columns = [
                  {
                    field: 'Codigo',
                    enableCellEdit: false,
                    enableColumnMenu: false,
                    type: 'number',
                    width: 50
                  },
                  {
                    field: 'Nombres',
                    enableCellEdit: false,
                    enableColumnMenu: false,
                    width: 200
                  },
                ];
                for (var i = 0; i < diarios.length; i++) {
                  vm.columns.push({
                      field: diarios[i],
                      enableSorting: false,
                      enableColumnMenu: false,
                      enableCellEditOnFocus:false,
                      visible: false,
                  });
                }
                vm.gridOptions.columnDefs = vm.columns;
                vm.generar_pauta_multiple();
              }
          }
        );
        //cargamos las columnas
      }

      vm.generar_pauta_multiple = function(){
        //generamos las columnas
        var datos = [];
        var row = [];
        for (var i = 0; i < vm.canillas.length; i++) {
          row = [];
          row['Codigo'] = vm.canillas[i].cod;
          row['Nombres'] = vm.canillas[i].name;
          for (var j = 0; j < vm.canillas[0].product.length; j++) {
              row[vm.canillas[0].product[j]] = vm.canillas[i].count[j]
          }
          datos.push(row)
        }

        vm.gridOptions.data = datos;
      }

      vm.exportar = function(){
          vm.gridApi.exporter.pdfExport('all', 'selected');
      }
      vm.exportarExcel = function(){
          vm.gridApi.exporter.csvExport('all', 'selected');
      }
    }
}())

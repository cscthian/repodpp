(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("HistorialCtrl",  ['$http','uiGridConstants', HistorialCtrl]);

    function HistorialCtrl($http,uiGridConstants){
      var vm = this;

      //inicialiamos nuestra tabla
      vm.columns = [
          { field: 'Codigo',enableCellEdit: false,enableColumnMenu: false, width: 100 },
          { field: 'Nombres', enableCellEdit: false,enableColumnMenu: false,headerCellClass: vm.highlightFilteredHeader},
          { field: 'Tipo', enableCellEdit: false,enableColumnMenu: false},
      ];
      vm.gridOptions = {
        enableFiltering: true,
        infiniteScrollRowsFromEnd: 40,
        infiniteScrollUp: true,

        enableSorting: true,
        columnDefs: vm.columns,
        enableGridMenu: true,
        enableSelectAll: false,
        exporterMenuCsv: false,
        exporterMenuPdf: false,
        exporterPdfDefaultStyle: {fontSize: 9},
        exporterPdfTableStyle: {margin: [10, 30, 30, 30]},
        exporterPdfTableHeaderStyle: {fontSize: 10, bold: true, italics: true, color: 'red'},
        exporterPdfHeader: { text: "DPP:  Historial de Canillas", style: 'headerStyle' },
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
      vm.generar_ranking = function(){
        $http.get("/api/reportes/canillas/historial/")
          .then(function(response){
              vm.ranking = response.data;

              if (vm.ranking.length > 0) {
                var months = vm.ranking[0].meses
                var meses = new Array ("Ene","Feb","Mar","Abr","May",
                                        "Jun","Jul","Ago","Sep",
                                        "Oct","Nov","Dic");

                for (var i = 0; i < months.length; i++) {
                  var mes = parseInt(months[i]);
                  vm.columns.push({
                    field: meses[mes-1],
                    enableSorting: false,
                    enableColumnMenu: false,
                    enableCellEditOnFocus:false
                  });
                }
                vm.generar_datos();
              }
          }
        );
        //cargamos las columnas
      }

      vm.generar_datos = function(){
        var meses = new Array ("Ene","Feb","Mar","Abr","May",
                                "Jun","Jul","Ago","Sep",
                                "Oct","Nov","Dic");
        //generamos las columnas
        var datos = [];
        var row = [];
        for (var i = 0; i < vm.ranking.length; i++) {
          row = [];
          row['Codigo'] = vm.ranking[i].cod;
          row['Nombres'] = vm.ranking[i].name;
          row['Tipo'] = vm.ranking[i].tipo;

          for (var j = 0; j < vm.ranking[0].puntaje.length; j++) {
              console.log(vm.ranking[i].puntaje[j]);
              row[meses[parseInt(vm.ranking[0].meses[j])-1]] = vm.ranking[i].puntaje[j];
          }
          datos.push(row)
        }

        vm.gridOptions.data = datos;
      }

      vm.exportar_pdf= function(){
          vm.gridApi.exporter.pdfExport('all', 'selected');
      }
      vm.exportarExcel = function(){
          vm.gridApi.exporter.csvExport('all', 'selected');
      }
    }
}())

(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("ConstatarCtrl",  ['$http','uiGridConstants','ngToast', ConstatarCtrl]);

    //MagazineCtrl.$inject = ["NgTableParams"];

    function ConstatarCtrl($http,uiGridConstants,ngToast){
      var vm = this;

      vm.validar = true;

      vm.gridOptions = {
        infiniteScrollRowsFromEnd: 40,
        infiniteScrollUp: true,
        columnDefs : [
          {
            name: 'guia',
            enableColumnMenu: false,
            displayName: 'Numero Guia',
            enableCellEdit: false,
            width: 150
          },
          {
            name: 'pk_diario',
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
            name: 'count',
            displayName: 'Cantidad Calculada',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false
          },
          {
            name: 'real_count',
            displayName: 'Cantidad Real',
            enableColumnMenu: false,
            enableCellEditOnFocus:false
          },
          {
            name: 'missing',
            displayName: 'Diferencia',
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
        exporterPdfHeader: { text: "Inventario Productos y Diarios", style: 'headerStyle' },
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
      vm.cargar_guia = function(numero){
        $http.get("/api/kardex/constatar/"+numero)
          .then(function(response){
              vm.class = "alert alert-success alert-sm";
              vm.mensaje = "Consulta Exitosa!!!"
              vm.gridOptions.data = response.data;
          }
        )
          .catch(function(fallback) {
            vm.class = "alert alert-danger alert-sm";
            vm.mensaje = "Error Verifique el Numero-Serie";
            vm.gridOptions.data = [];
          });
        }
      vm.gridOptions.enableCellEditOnFocus = true;
      vm.currentFocused = "";

      vm.gridOptions.onRegisterApi = function(gridApi){
        vm.gridApi = gridApi;

        gridApi.edit.on.afterCellEdit(null,function(rowEntity, colDef, newValue, oldValue){
          if (colDef.name == "real_count") {
              //validamos
              rowEntity.missing = rowEntity.count - rowEntity.real_count;
              if (rowEntity.missing<0) {
                  vm.validar = false;
              }
              else {
                  vm.validar = true;
              }
          }
        });
      };

      vm.enviar_data = function(){
          $http.post("/api/kardex/constatar/save", vm.gridOptions.data)
              .success(function(res){
                vm.gridOptions.data = [];
                ngToast.create('se guardo la Entrega correctamente');
              })
              .catch(function(fallback) {
                vm.class = "alert alert-danger alert-sm";
                vm.mensaje= "Nose Puede Gurdar La inforacion Verifique los datos";
              });;

      }

      vm.exportar = function(){
          vm.gridApi.exporter.pdfExport('all', 'selected');
      }

    }
}())

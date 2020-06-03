(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("RegisEntregaProdCtrl",  ['$http','uiGridConstants','ngToast','$window',RegisEntregaProdCtrl]);

    function RegisEntregaProdCtrl($http,uiGridConstants,ngToast,$window,hotkeys){
      var vm = this;
      var codCanilla;

      vm.class = "alert alert-success alert-sm";
      vm.mensaje = '';
      vm.alerta = '';
      vm.usuario = '-1'
      var total_count = 0;
      vm.validado = false;

      vm.enter = function(keyEvent,tipo) {
        if (keyEvent.which === 13){
            vm.cargar_pauta(vm.codigo,vm.usuario,tipo);
        }
      }

      vm.enter2 = function(keyEvent) {
        if (keyEvent.which === 13){
            vm.enviar_data();
        }
      }

      vm.gridOptions = {
        infiniteScrollRowsFromEnd: 10,
        infiniteScrollUp: true,
        columnDefs : [
          {
            name: 'magazine',
            enableColumnMenu: false,
            cellClass:'big_black',
            displayName: 'Diarios Productos',
            enableCellEdit: false,
            width: 400
          },
          {
            name: 'precio_venta',
            cellClass:'precio_black',
            displayName: 'Precio (S/.)',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 120
          },
          {
            name: 'count',
            cellClass:'count_black',
            displayName: 'Entregado',
            enableColumnMenu: false,
            enableCellEdit: true,
            enableCellEditOnFocus:false,
            width: 120
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
        exporterPdfHeader: { text: "Pauta de Producto", style: 'headerStyle' },
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

      vm.cargar_usuario = function(usuario){
        vm.usuario = usuario;
      }
      //cargamos la lista de canillas
      vm.cargar_pauta = function(codigo,usuario,tipo){
        vm.gridOptions.data = [];
        vm.gridOptions.rowHeight = 50;
        vm.mje = "";
        vm.dni = "";
        vm.total_count = 0;
        vm.validado = false;
        //cargamos el usuario
        vm.usuario = usuario;
        //convertimos codigo a coodio legible para BD
        if (codigo.length < 3) {
          if (codigo.length == 1) {
            codigo = '00'+codigo;
          }
          else {
            codigo = '0'+codigo;
          }
        }
        //peticion get
        $http.get("/api/pauta/cargar-entrega/"+codigo+"/"+tipo+"/")
          .then(function(response){
              codCanilla=codigo;
              vm.class = "alert alert-success alert-sm";
              vm.vendedor = response.data[0].vendor;
              vm.gridOptions.data = response.data;
          }
        )
        .catch(function(fallback) {
          vm.class = "alert alert-danger alert-sm";
          vm.vendedor = "Error Verifique el Codigo, o el Cliente no tiene Pauta";
          vm.gridOptions.data = [];
        });
      }

      //capturamos el evento de cambio de datos
      vm.gridOptions.onRegisterApi = function(gridApi){
        vm.gridApi = gridApi;

        gridApi.edit.on.afterCellEdit(null,function(rowEntity, colDef, newValue, oldValue){
          vm.mensaje = '';
          vm.vencido = false;
          vm.not_orden = false;
          vm.alerta = '';
          total_count = 0;
          for (var i = 0; i < vm.gridOptions.data.length; i++) {
            total_count = total_count + parseInt(vm.gridOptions.data[i].count);
          }
          vm.validar_data();
        });

      };

      vm.validar_data = function(){
          vm.mje = "";
          if (vm.dni != null) {
            if (vm.dni.length != 8){
                vm.validado = false;
                console.log(vm.validado);
                vm.mje = "Ingrese un Dni Valido"
                return false;
            }
            else {
              if (isNaN(total_count)) {
                console.log('**** '+total_count);
                vm.validado = false;
                vm.mje = "Las Cantidades de Entrega Deben ser Numeros"
                return false;
              }
              else {
                vm.validado = true;
                vm.mje = "";
                return true;
              }
            }
          }
          else {
            vm.validado = false;
            vm.mje = "Por Favor Ingrese Dni Del Receptor"
            return false;
          }
      }

      //para colo toda las cantidades en cero
      vm.limpiar = function(){
        for (var i = 0; i < vm.gridOptions.data.length; i++) {
          vm.gridOptions.data[i].count = 0;
        }
      }

      vm.enviar_data = function(){
        vm.validar_data();
        if (vm.validado) {
          $http.post("/api/asignacion/producto-save/"+codCanilla+"/"+vm.dni+"/", vm.gridOptions.data)
              .success(function(res){
                vm.gridOptions.data = [];
                vm.dni = "";
                total_count = 0;
                ngToast.create('se guardo la Entrega');
              })
              .catch(function(fallback) {
                vm.class = "alert alert-danger alert-sm";
                vm.vendedor = "Nose Puede Gurdar La inforacion Verifique los datos";
                console.log(fallback);
              });
        }
        else {
          ngToast.create({
            className: 'danger',
            content: "Error, Verifique que los datos sean Numeros",
          });
        }
      }

    }

}())

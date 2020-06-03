(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("CobrosCtrl",  ['$http','uiGridConstants','ngToast','$window',CobrosCtrl]);

    function CobrosCtrl($http,uiGridConstants,ngToast,$window,hotkeys){
      var vm = this;

      vm.class = "alert alert-success alert-sm";
      vm.boleta = 0;
      vm.pago = 0;
      vm.deuda = 0;
      vm.mensaje = '';
      vm.alerta = '';
      vm.vencido = false;
      vm.not_orden = false;
      vm.por_vencer = [];
      vm.usuario = '-1'


      vm.enter = function(keyEvent) {
        if (keyEvent.which === 13){
            vm.cargar_movimientos(vm.codigo,vm.usuario);
        }
      }

      //metodo para calcular el vuelto
      vm.calcular_vuelto = function(){
        vm.vuelto = vm.pago_con - vm.cobrar;
        vm.vuelto = vm.vuelto.toFixed(3);
      }

      vm.gridOptions = {
        infiniteScrollRowsFromEnd: 10,
        infiniteScrollUp: true,
        columnDefs : [
          {
            name: 'tipo',
            enableColumnMenu: false,
            displayName: 'Tipo',
            enableCellEdit: false,
            sort: {
              direction: uiGridConstants.ASC,
              priority: 0
            },
            width: 55
          },
          {
            name: 'estado',
            cellClass: function(grid, row, col, rowRenderIndex, colRenderIndex) {
              if (grid.getCellValue(row,col) === 'VENCIDO') {
                return 'blue';
              }
              else {
                return 'blank';
              }
            },
            enableColumnMenu: false,
            displayName: 'Estado',
            enableCellEdit: false,
            width: 70
          },
          {
            name: 'guide',
            cellClass:'black',
            enableColumnMenu: false,
            displayName: 'Guia',
            enableCellEdit: false,
            visible: false,
            width: 100
          },
          {
            name: 'date',
            cellClass:'black',
            enableColumnMenu: false,
            displayName: 'Fecha',
            enableCellEdit: false,
            sort: {
              direction: uiGridConstants.ASC,
              priority: 1
            },
            width: 90
          },
          {
            name: 'diario',
            enableColumnMenu: false,
            cellClass:'black',
            displayName: 'Diarios Productos',
            enableCellEdit: false,
            width: 250
          },
          {
            name: 'precio_venta',
            cellClass:'black',
            displayName: 'Precio',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 70
          },
          {
            name: 'amount',
            cellClass:'black',
            displayName: 'Monto',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 70
          },
          {
            name: 'entregado',
            cellClass:'black',
            displayName: 'Entregado',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 100
          },
          {
            name: 'devuelto',
            cellClass:'black',
            displayName: 'Devuelto',
            enableColumnMenu: false,
            enableCellEditOnFocus:false
          },
          {
            name: 'pagar',
            cellClass:'black',
            displayName: 'Pagar',
            enableColumnMenu: false,
            enableCellEditOnFocus:false
          },
          {
            name: 'deuda',
            cellClass:'black',
            displayName: 'A cuenta',
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
        exporterPdfHeader: { text: "Deudas vendedor", style: 'headerStyle' },
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
      vm.cargar_movimientos = function(codigo,usuario){
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
        $http.get("/api/pagos/movimientos/"+codigo)
          .then(function(response){
              vm.codCanilla=codigo;
              vm.class = "alert alert-success alert-sm";
              vm.vendedor = response.data[0].canilla;
              vm.boleta = response.data[0].boleta;

              vm.gridOptions.data = response.data;
              vm.fecha = new Date();

              vm.pago = 0.00;
              vm.deuda = 0.00;
              vm.por_vencer = response.data[vm.gridOptions.data.length -1].por_vencer;
              for (var i = 0; i < vm.gridOptions.data.length; i++) {
                vm.pago = vm.pago + (vm.gridOptions.data[i].pagar * vm.gridOptions.data[i].precio_venta);
                //vm.deuda = vm.deuda + (vm.gridOptions.data[i].deuda * vm.gridOptions.data[i].precio_venta);
              }
              //redondeamos el resultado
              vm.pago = vm.pago.toFixed(3);
              //cargamos voucher por defecto
              vm.cargar_voucher();
              vm.cobrar = vm.pago;
          }
        )
        .catch(function(fallback) {
          vm.class = "alert alert-danger alert-sm";
          vm.vendedor = "Error Verifique el Codigo, o el Cliente no tiene Deudas";
          vm.gridOptions.data = [];
        });
      }

      vm.gridOptions.enableCellEditOnFocus = true;

      vm.currentFocused = "";

      vm.gridOptions.onRegisterApi = function(gridApi){
        vm.gridApi = gridApi;

        gridApi.edit.on.afterCellEdit(null,function(rowEntity, colDef, newValue, oldValue){
          vm.mensaje = '';
          vm.vencido = false;
          vm.not_orden = false;
          vm.alerta = '';
          if (colDef.name == "devuelto") {
              rowEntity.pagar = rowEntity.entregado - rowEntity.devuelto;
              rowEntity.deuda = rowEntity.entregado - rowEntity.devuelto - rowEntity.pagar;
              rowEntity.amount = rowEntity.pagar*rowEntity.precio_venta;
          }
          else {
              rowEntity.deuda = rowEntity.entregado - rowEntity.devuelto - rowEntity.pagar;
              rowEntity.amount = rowEntity.pagar*rowEntity.precio_venta;
          }

          vm.pago = 0.00;
          vm.deuda = 0.00;
          vm.deudas = [];
          for (var i = 0; i < vm.gridOptions.data.length; i++) {
            vm.pago = vm.pago + (vm.gridOptions.data[i].pagar * vm.gridOptions.data[i].precio_venta);
            if (vm.gridOptions.data[i].tipo == 'Diario') {
              vm.deuda = vm.deuda + (vm.gridOptions.data[i].deuda * vm.gridOptions.data[i].precio_venta);
            }
            else {
              // if (vm.gridOptions.data[i].vencido == true) {
              //   vm.deuda = vm.deuda + (vm.gridOptions.data[i].deuda * vm.gridOptions.data[i].precio_venta);
              // }
              if ((vm.usuario != '4')) {
                vm.deuda = vm.deuda + (vm.gridOptions.data[i].deuda * vm.gridOptions.data[i].precio_venta);
              }
              else {
                if (vm.gridOptions.data[i].vencido == true) {
                  vm.deuda = vm.deuda + (vm.gridOptions.data[i].deuda * vm.gridOptions.data[i].precio_venta);
                }
              }
            }

            //veificamos si vencio
            if ((vm.gridOptions.data[i].vencido == true) && (vm.gridOptions.data[i].devuelto > 0) && (vm.usuario !='4')){
                vm.mensaje = 'Diario '+vm.gridOptions.data[i].diario+' VENCIDO no se pude devolver';
                vm.vencido = true;
            }
            //generamos arreglo de vencido
            if ((vm.gridOptions.data[i].deuda > 0)){
                vm.deudas.push(
                  {
                    'name':'DEBE--'+vm.gridOptions.data[i].diario+'('+vm.gridOptions.data[i].deuda+')',
                  }
                )
            }
            //verificamos si numero negativo
            if (((vm.pago < 0) || (vm.deuda < 0)) && (vm.gridOptions.data[i].precio_venta)>=0){
                vm.mensaje = 'El PAGO o la DEUDA no pueden ser negativos';
                vm.vencido = true;
            }

          }
          //redondeamos el resultado
          vm.pago = vm.pago.toFixed(3);
          vm.deuda = vm.deuda.toFixed(3)
          vm.cargar_voucher();
          vm.cobrar = vm.pago;
        });
        //actualizamos voucher

      };

      vm.validar_data = function(){
          var validado = true;
          //validamos el grid
          if (isNaN(vm.pago) || isNaN(vm.deuda)){
              console.log(vm.pago);
              console.log(vm.deuda);
              validado = false;
          }
          else {
            validado = true;
          }
          return validado;
      }

      vm.enviar_data = function(codigo){
        if (vm.validar_data()) {
          $http.post("/api/pagos/save/"+vm.codCanilla+"/", vm.gridOptions.data)
              .success(function(res){
                vm.gridOptions.data = [];
                vm.pago = 0.00;
                vm.deuda = 0.00;
                vm.deudas = [];
                vm.por_cobrar = [];
                ngToast.create('se guardo el Pago correctamente');
              })
              .catch(function(fallback) {
                vm.class = "alert alert-danger alert-sm";
                vm.vendedor = "Nose Puede Gurdar La inforacion Verifique los datos";
              });
        }
        else {
          ngToast.create({
            className: 'danger',
            content: "Error, Verifique que los datos sean Numeros",
          });
        }

      }

    vm.guardar_print = function(){
      if (vm.validar_data()) {
        vm.cargar_voucher();
        $http.post("/api/pagos/save/"+vm.codCanilla+"/", vm.gridOptions.data)
            .success(function(res){
              vm.gridOptions.data = [];
              vm.pago = 0.00;
              vm.deuda = 0.00;
              vm.deudas = [];
              vm.por_cobrar = [];
              vm.printDiv('print-section');
              ngToast.create('se guardo la Entrega correctamente');
              window.location.href = '/caja/cobros/cobrar/cobros';
            })
            .catch(function(fallback) {
              vm.class = "alert alert-danger alert-sm";
              vm.vendedor = "Nose Puede Gurdar La inforacion Verifique los datos";
            });;
      }
      else {
        ngToast.create({
          className: 'danger',
          content: "Error, Verifique que los datos sean Numeros",
        });
      }

    }

    //funcion rearma un texto
    vm.cut_text = function(texto, tipo){
      var caracter = texto.split("");
      var first = '';
      var second = '-';
      for (var i = 0; i < caracter.length; i++) {
        if (tipo == 'Diario') {
          if (i < 6) {
            first = first + caracter[i];
          }
          else {
            if (caracter[i] == '[') {
              second = second + caracter[i+1] + caracter[i+2];
            }
          }
        }
        else {
          if (i < 6) {
            first = first + caracter[i];
          }
          else {
            if ((i+3)-caracter.length==1) {
              second = second + caracter[caracter.length-3] + caracter[caracter.length-2] + caracter[caracter.length-1];
            }
          }
        }

      }
      return first+second;
    }

    //cargar recibo por defecto
    vm.cargar_voucher=function(){
      vm.items = [];
      for (var i = 0; i < vm.gridOptions.data.length; i++) {
          var sub_total = vm.gridOptions.data[i].pagar*vm.gridOptions.data[i].precio_venta;
          sub_total = sub_total.toFixed(2)
          if ((vm.gridOptions.data[i].pagar > 0) ||(vm.gridOptions.data[i].devuelto >0)) {
            var rows = {
              'item':vm.cut_text(vm.gridOptions.data[i].diario,vm.gridOptions.data[i].tipo),
              'dev':vm.gridOptions.data[i].devuelto.toString(),
              'pag':vm.gridOptions.data[i].pagar.toString(),
              'pu':vm.gridOptions.data[i].precio_venta.toString(),
              'sub':sub_total.toString(),
            };
            vm.items.push(rows);
          }
      }
    }

    //metodo de impresion directa de html
    vm.printDiv = function(divName) {
      var printContents = document.getElementById(divName).innerHTML;
      var originalContents = document.body.innerHTML;
      document.body.innerHTML = printContents;
      window.print();
      document.body.innerHTML = originalContents;
    }

    }
}())

(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("VoucherAddCtrl",  ['$http','$window','ngToast', VoucherAddCtrl]);

    function VoucherAddCtrl($http,$window,ngToast){
      var vm = this;

      var total = 0;

      vm.voucher_json = [];

      var lis_guides = [];
      vm.no_valido = false;

      vm.gridOptions = {
        columnDefs : [
          {
            name: 'guide',
            displayName: 'N° Guia',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 110
          },
          {
            name: 'date',
            displayName: 'Fecha Rec.',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 90
          },
          {
            name: 'magazine',
            displayName: 'Item',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 130
          },
          {
            name: 'count',
            displayName: 'Can. Recep',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            type: 'number',
          },
          {
            name: 'precio_unitario',
            displayName: 'Precio U',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            type: 'number',
          },
          {
            name: 'devuelto',
            displayName: 'Devol',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            type: 'number',
          },
          {
            name: 'vendido',
            displayName: 'Vend',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            type: 'number',
          },
          {
            name: 'amount_vendido',
            displayName: 'Total Ven.',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            type: 'number',
          },
          {
            name: 'amount',
            displayName: 'Monto Cal.',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
          },
          {
            name: 'voucher',
            displayName: 'Num. Voucher',
            enableColumnMenu: true,
            enableCellEdit: true,
            enableCellEditOnFocus:true,
          },
        ],
        //personalizamos el pdf
        infiniteScrollRowsFromEnd: 10,
        enableHorizontalScrollbar: true,
        infiniteScrollUp: true,
        enableGridMenu: true,
        exporterPdfDefaultStyle: {fontSize: 9},
        exporterPdfTableStyle: {margin: [10, 30, 10, 30]},
        exporterPdfTableHeaderStyle: {fontSize: 10, bold: true, italics: true, color: 'red'},
        exporterPdfHeader: { text: "Liquidacion Modulo Caja DPP", style: 'headerStyle' },
        exporterPdfFooter: function ( currentPage, pageCount ) {
          return { text: currentPage.toString() + ' de ' + pageCount.toString(), style: 'footerStyle' };
        },
        exporterPdfCustomFormatter: function ( docDefinition ) {
          docDefinition.styles.headerStyle = { fontSize: 13, bold: true, margin: [20, 20, 10, 10] };
          docDefinition.styles.footerStyle = { fontSize: 10, bold: true };
          return docDefinition;
        },
        exporterPdfOrientation: 'landscape',
        exporterPdfPageSize: 'LETTER',
        exporterPdfMaxGridWidth: 600,

        onRegisterApi: function(gridApi) {
          vm.gridApi = gridApi;
        }
      };

      //funcion que consulta guias en rango de fechas
      vm.liquidacion_dia = function(parametro){
        console.log('----'+parametro);
        var date1;
        if (parametro == null) {
          var d1 = new Date()
           date1 = d1.getDate() + "-" + (d1.getMonth()+1) + "-" + d1.getFullYear();
           console.log('liquif¿dacio caja');
        }
        else {
          var d1 = new Date(vm.fecha)
           date1 = d1.getDate() + "-" + (d1.getMonth()+1) + "-" + d1.getFullYear();
           console.log('liquidacion admin');
        }

        $http.get("/api/caja/liuidacion/dia/"+date1+'/')
          .then(function(response){
            vm.gridOptions.data = response.data;
          }
        )
        .catch(function(fallback) {
          console.log('error');
        });
      }


      //funcion que suma valores
      vm.calcular_total = function(){
          total = 0;
          for (var i = 0; i < vm.gridOptions.data.length; i++) {
            if (vm.gridOptions.data[i].amount != ' ') {
              console.log('---'+vm.gridOptions.data[i].amount);
              total = total + parseFloat(vm.gridOptions.data[i].amount);
            }

          }
          return total;
      }


      //funcion para cargar guias registros por fecha
      vm.cargar_data = function(){
          var date1 = vm.fecha.getFullYear() + "-" + (vm.fecha.getMonth()+1) + "-" + vm.fecha.getDate();
          var voucher_registrados;
          $http.get("/api/voucher/recuperar/"+date1+'/')
            .then(function(response){
                voucher_registrados = response.data;
                //mostramos los datos cargados
                for (var i = 0; i < vm.gridOptions.data.length; i++) {
                  for (var j = 0; j < voucher_registrados.length; j++) {
                    if ((vm.gridOptions.data[i].amount != ' ') && (vm.gridOptions.data[i].guide==voucher_registrados[j].guide)) {
                      vm.gridOptions.data[i].voucher = voucher_registrados[j].voucher;
                    }
                  }
                }
            }
          );
      }

      //funion que calcula la cantidad de guias
      vm.listar_guias = function(){
          var date1 = vm.fecha.getFullYear() + "-" + (vm.fecha.getMonth()+1) + "-" + vm.fecha.getDate();
          vm.voucher_json = [];
          console.log('------'+date1);
          for (var i = 0; i < vm.gridOptions.data.length; i++) {
            if (vm.gridOptions.data[i].amount != ' ') {
              lis_guides.push(vm.gridOptions.data[i].guide);
            }
            if ((vm.gridOptions.data[i].voucher != null) && (vm.gridOptions.data[i].voucher.length > 0))  {
              vm.voucher_json.push(
                {
                  'guide':vm.gridOptions.data[i].guide,
                  'voucher':vm.gridOptions.data[i].voucher,
                  'date':date1,
                }
              );
            }
          }
      }

      //funcion para generar un json a enviar
      vm.gridOptions.onRegisterApi = function(gridApi){
        vm.gridApi = gridApi;

        gridApi.edit.on.afterCellEdit(null,function(rowEntity, colDef, newValue, oldValue){
          vm.mensaje = '';
          vm.no_valido = false;
          if ((colDef.name == "voucher") && (rowEntity.voucher != null)) {
            vm.validar_voucher();
          }
        });
      }

      //funcion para validar los datos de la tabla
      vm.validar_voucher = function(){
        //iteramos voucher json y genreamos nuevo json
        vm.mensaje = '';
        vm.no_valido = false;
        lis_guides = [];
        vm.listar_guias();
        //variable que se envia al servidor
        for (var i = 0; i < lis_guides.length; i++) {
          //variable que verifica las veces que se repirte una guia
          var k = 0
          for (var j = 0; j < vm.voucher_json.length; j++) {
            if (lis_guides[i] == vm.voucher_json[j].guide) {
                k++;
            }
          }
          //validamos
          if (k > 1) {
            vm.mensaje = 'La Guia: '+lis_guides[i]+' Tine Dos Voucher';
            vm.no_valido = true;
          }
          else {
            if (k < 1) {
              vm.mensaje = 'La Guia: '+lis_guides[i]+' No Tiene Voucher';
              vm.no_valido = true;
            }
          }
        }
      }

      vm.enviar_data = function(){
        vm.validar_voucher();
        if (vm.no_valido == false) {
          $http.post("/api/save/voucher/", vm.voucher_json)
              .success(function(res){
                if (res.id=='0') {
                  ngToast.create(res.respuesta);
                  $window.location.reload();
                }
                else {
                  vm.no_valido = true;
                  vm.mensaje = res.respuesta;
                }
                //$location.href
              })
              .error(function(res){
                vm.no_valido = true;
                vm.mensaje = 'Error Verifique los Datos';
              });
        }
      }

      //metodo para guardar borrador
      vm.guardar_data = function(){
          $http.post("/api/save/voucher/", vm.voucher_json)
              .success(function(res){
                if (res.id=='0') {
                  ngToast.create(res.respuesta);
                  $window.location.reload();
                }
                else {
                  vm.mensaje = res.respuesta;
                }
                //$location.href
              })
              .error(function(res){
                vm.mensaje = 'Error Verifique los Datos';
              });
      }


      //funcion para exportar
      vm.exportar_pdf = function(){
        var date1
        if (vm.fecha != null) {
          var d1 = new Date(vm.fecha)
          date1 = d1.getDate() + "/" + (d1.getMonth()+1) + "/" + d1.getFullYear();
        }
        else {
          var d1 = new Date()
          date1 = d1.getDate() + "/" + (d1.getMonth()+1) + "/" + d1.getFullYear();
        }
        vm.calcular_total();

        vm.gridOptions.exporterPdfHeader.text = "Liquidacion Modulo Caja Proveedor DPP: "+" de ["+date1+"]"+" Total: S/."+total.toFixed(3)+"  "+
        " Caja: ...............  "+" Control: ............... ";
        vm.gridOptions.exporterPdfHeader.style = 'headerStyle'
        vm.gridApi.exporter.pdfExport('all', 'selected');
      }
      vm.exportarExcel = function(){
        vm.gridApi.exporter.csvExport('all', 'selected');
      }
    };
}())

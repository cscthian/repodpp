(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("LiquidacionDiaCtrl",  ['$http', '$window',LiquidacionDiaCtrl]);

    function LiquidacionDiaCtrl($http,$window){
      var vm = this;

      vm.date = new Date();

      var total = 0;

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


//===============================================================================//
//===============================================================================//
//===============================================================================//
  //funcion que consulta guias en rango de fechas
    vm.liquidacion_por_dia = function(parametro){
      var date1;
      if (parametro == null) {
        var d1 = new Date()
        date1 = d1.getDate() + "-" + (d1.getMonth()+1) + "-" + d1.getFullYear();
      }
      else {
        var d1 = new Date(parametro)
        date1 = d1.getDate() + "-" + (d1.getMonth()+1) + "-" + d1.getFullYear();
      }

      //inicializamos monto cobrado
      vm.monto_cobrado = 0;
      vm.total_devuelto = 0;
      $http.get("/api/caja/liuidacion-proveedor/"+date1+'/')
        .then(function(response){
          vm.liquidacion = response.data;
          for (var i = 0; i < vm.liquidacion.length; i++) {
            vm.monto_cobrado = parseFloat(vm.monto_cobrado) + parseFloat(vm.liquidacion[i].sub_total);
            vm.monto_cobrado = vm.monto_cobrado.toFixed(3);
            for (var j = 0; j < vm.liquidacion[i].lista_pagos.length; j++) {
              vm.total_devuelto = parseInt(vm.total_devuelto) +  parseInt(vm.liquidacion[i].lista_pagos[j].devuelto);
            }
          }
        }
      )
      .catch(function(fallback) {
        console.log('error');
      });
    }

    //verificar si es venta caja
    vm.venta_caja = function(texto){
      console.log('comprobando venta caja'+texto);
      if (texto == '[VENTA-CAJA]') {
        return true;
      }
      else {
        return false;
      }
    }
    //imprimir funcion
    vm.imprimir = function(){
      vm.printDiv('print-section');
      window.location.reload();
    }

    vm.printDiv = function(divName) {
      var printContents = document.getElementById(divName).innerHTML;
      var originalContents = document.body.innerHTML;
      document.body.innerHTML = printContents;
      window.print();
      document.body.innerHTML = originalContents;
    }
    };
}())

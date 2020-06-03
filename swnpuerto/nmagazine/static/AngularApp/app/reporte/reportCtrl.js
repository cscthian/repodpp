(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("ReportCtrl",  ['$http','uiGridConstants','ngToast', ReportCtrl]);

    //MagazineCtrl.$inject = ["NgTableParams"];

    function ReportCtrl($http,uiGridConstants,ngToast){
      var vm = this;

      vm.gridOptions = {
        columnDefs : [
          {
            name: 'pk',
            enableColumnMenu: false,
            sort: {
              direction: uiGridConstants.ASC,
              priority: 0
            },
            displayName: '#Registro',
            enableCellEdit: false,
            width: 90
          },
          {
            name: 'magazine',
            displayName: 'Producto',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false
          },
          {
            name: 'date',
            displayName: 'Fecha Registro',
            enableColumnMenu: false,
            enableCellEditOnFocus:false
          },
          {
            name: 'input',
            displayName: 'Entrada',
            enableColumnMenu: false,
            enableCellEditOnFocus:false
          },
          {
            name: 'output',
            displayName: 'Salida',
            enableColumnMenu: false,
            enableCellEditOnFocus:false
          },
          {
            name: 'total',
            displayName: 'Diferencia',
            enableColumnMenu: false,
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
        exporterPdfHeader: { text: "Pauta de entrega", style: 'headerStyle' },
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

      vm.generar_kardex = function(codigo){
        // $http.get("/api/kardex/"+codigo)
        //   .then(function(response){
        //       vm.gridOptions.data = response.data;
        //   }
        // );
        vm.gridOptions.data = [
          {
            'pk':'1',
            'magazine':'PERU 21',
            'date':'12/09/19',
            'input':'100',
            'output':'30',
            'total':'100',
          },
          {
            'pk':'2',
            'magazine':'PERU 21',
            'date':'12/09/19',
            'input':'100',
            'output':'30',
            'total':'100',
          },
          {
            'pk':'3',
            'magazine':'PERU 21',
            'date':'12/09/19',
            'input':'100',
            'output':'30',
            'total':'100',
          },
        ];
      }

      vm.gridOptions.enableCellEditOnFocus = true;
      vm.currentFocused = "";

      vm.exportar = function(){
          vm.gridApi.exporter.pdfExport('all', 'selected');
      }

    }
}())

(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("PanelCtrl",  ['$http', PanelCtrl]);

    function PanelCtrl($http){
      var vm = this;
      vm.datos = [];

      vm.cargar_datos = function(){
        $http.get("/api/administrador/ventas/")
          .then(function(response){
              vm.myDataSource.data  = response.data;
              console.log('entro');
          }
        );
      }
      vm.myDataSource = {
                chart: {
                    caption: "Reporte de Semana",
                    subCaption: "Top 5 ultimos 5 dias",
                    "xAxisName": "Dias (Fecha Mes)",
                    "yAxisName": "Venta Neta (Soles)",
                    "numberPrefix": "S/.",
                    "theme": "fint",
                    "paletteColors": "#398531",
                    "bgColor": "#ffffff",
                    "showBorder": "0",
                    "showCanvasBorder": "0",
                    "plotBorderAlpha": "10",
                    "usePlotGradientColor": "0",
                },
              };

    };
}())

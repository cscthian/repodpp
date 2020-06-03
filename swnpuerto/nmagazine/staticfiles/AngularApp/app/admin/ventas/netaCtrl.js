(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("NetaCtrl",  ['$http', NetaCtrl]);

    function NetaCtrl($http){
      var vm = this;

      //funcion que grafica reporte
      vm.cargar_venta_neta = function(){
        $http.get("/api/ventas/cierre/venta-neta/")
          .then(function(response){
              vm.myDataSource.data  = response.data;
          }
        );
      }
      vm.myDataSource = {
        chart: {
            caption: "Reporte Venta Neta",
            subCaption: "Top 5 ultimos meses",
            "xAxisName": "Mes",
            "yAxisName": "Venta Neta (Soles)",
            "numberPrefix": "S/.",
            "paletteColors": "#0075c2",
            "bgColor": "#ffffff",
            "showBorder": "0",
            "showCanvasBorder": "0",
            "plotBorderAlpha": "10",
            "usePlotGradientColor": "0",
            "plotFillAlpha": "50",
            "showXAxisLine": "1",
            "axisLineAlpha": "25",
            "divLineAlpha": "10",
            "showValues": "1",
            "showAlternateHGridColor": "0",
            "captionFontSize": "14",
            "subcaptionFontSize": "14",
            "subcaptionFontBold": "0",
            "toolTipColor": "#ffffff",
            "toolTipBorderThickness": "0",
            "toolTipBgColor": "#000000",
            "toolTipBgAlpha": "80",
            "toolTipBorderRadius": "2",
            "toolTipPadding": "5",
          },
      };
      //
      // vm.selectedValue = "nothing";
      // vm.events = {
      //   dataplotclick: function(ev, props) {
      //     vm.$apply(function() {
      //         vm.selectedValue = props.displayValue;
      //       });
      //     }
      // }

      //funcion que grafica reporte
      vm.cargar_margen_ganacia = function(){
        $http.get("/api/ventas/cierre/ingreso-neto/")
          .then(function(response){
              vm.myDataSource2.data  = response.data;
              console.log('entro');
          }
        );
      }
      vm.myDataSource2 = {
        chart: {
            caption: "Reporte Ingresos",
            subCaption: "Top 5 ultimos meses",
            "xAxisName": "Mes",
            "yAxisName": "Ingresos (Soles)",
            "numberPrefix": "S/.",
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

(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("CierreCtrl",  ['$http', CierreCtrl]);

    function CierreCtrl($http){
      var vm = this;

      // cargamos lista de CierreMes
      $http.get("/api/ventas/cierre/")
        .then(
            function(response){
              vm.cierres = response.data;
            }
        );

      //funcion que consulta guias en rango de fechas
      vm.consulta_montos = function(fecha1, fecha2){
        vm.error2 = false;
        var d1 = new Date(fecha1)
        var d2 = new Date(fecha2)
        var date1 = d1.getDate() + "-" + (d1.getMonth()+1) + "-" + d1.getFullYear();
        var date2 = d2.getDate() + "-" + (d2.getMonth()+1) + "-" + d2.getFullYear();
        $http.get("/api/liquidacion/detalle/"+date1+'/'+date2+'/')
          .then(function(response){
            console.log(response.data);
            vm.guias = response.data;
            //generamos la impresion
            vm.calcular_montos(vm.guias);
          }
        )
        .catch(function(fallback) {
          vm.mensaje2 = 'Datos Incorrectos';
        });
      }

    //funcion para calcular los montos
    vm.calcular_montos = function(lista){
      var ingreso = 0;
      var venta = 0;
      for (var i = 0; i < lista.length; i++) {
        var suma_ingreso = 0;
        var suma_venta = 0;
        for (var j = 0; j < lista[i].detalle.length; j++) {
          suma_ingreso = suma_ingreso + (lista[i].detalle[j].vendido*lista[i].detalle[j].precio_guia);
          suma_venta = suma_venta + (lista[i].detalle[j].vendido*lista[i].detalle[j].precio_venta);
        }
        ingreso = ingreso + suma_ingreso;
        venta = venta + suma_venta;
      }
      //actualimoz los valores
      vm.venta_real = venta.toFixed(3);
      var dif = venta - ingreso
      vm.ingreso_real = dif.toFixed(3);
    }

    };
}())

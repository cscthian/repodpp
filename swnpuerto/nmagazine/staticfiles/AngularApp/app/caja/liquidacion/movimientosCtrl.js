(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("MovimientosCtrl",  ['$http', MovimientosCtrl]);

    function MovimientosCtrl($http){
      var vm = this;

      var total = 0;

      //funcion que consulta guias en rango de fechas
      vm.generar_movimientos = function(){
        var d1 = new Date(vm.fecha)
        var date1 = d1.getFullYear() + "-" + (d1.getMonth()+1) + "-" + d1.getDate();
        $http.get("/api/caja/movimientos/"+date1+'/')
          .then(function(response){
            vm.movimientos_dia = response.data;
          }
        )
        .catch(function(fallback) {
          console.log('error');
        });
      }

      vm.devolver_dia = function(dia){
        var array_dias = ['Lun','Mar','Mier','Jue','Vie','Sab','Dom','Prod']
        return array_dias[parseInt(dia)]
      }
    };
}())

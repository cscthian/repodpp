(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("InventarioCtrl",  ['$http', InventarioCtrl]);

    //MagazineCtrl.$inject = ["NgTableParams"];

    function InventarioCtrl($http){
      var vm = this;
      // recuperamos el get del servidor
      $http.get("/api/kardex/inventario/")
        .then(
            function(response){
              vm.magazins = response.data;
            }
        );

      vm.cargar_detalle = function(codigo){
        $http.get("/api/kardex/inventario/dealle/"+codigo+"/")
          .then(function(response){
              vm.diarios = response.data;
              vm.diarios1 = response.data;
          }
        );
      }

      //filtramos por ragno de fechas
      vm.search_fecha = function(){
          if (vm.fecha1==null) {
              vm.fecha1 = new Date();
          }
          //realizamos la logica de filtro
          vm.diarios = [];
          for (var i = 0; i < vm.diarios1.length; i++) {
            var fecha = new Date(vm.diarios1[i].fecha);
            var fecha1 = new Date(vm.fecha1)
            if ((fecha1.getDate()==fecha.getDate()) && (fecha1.getMonth()==fecha.getMonth()) && (fecha.getFullYear()==fecha1.getFullYear())){
                vm.diarios.push(vm.diarios1[i]);
            }
          }
      }
    }
}())

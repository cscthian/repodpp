(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("MagazineCtrl",  ['$http', MagazineCtrl]);

    //MagazineCtrl.$inject = ["NgTableParams"];

    function MagazineCtrl($http){
      var vm = this;
      // recuperamos el get del servidor
      $http.get("/api/magazin")
        .then(
            function(response){
              vm.diarios = response.data;
              console.log(vm.diarios);
            }
        );

      vm.tipo_diario = function(variable){
        console.log(variable);
        if (variable=='Diario') {
          return true;
        }
        else {
          return false;
        }
      }
      vm.tipo_producto = function(variable){
        console.log(variable);
        if (variable=='Producto') {
          return true;
        }
        else {
          return false;
        }
      }
    }
}())

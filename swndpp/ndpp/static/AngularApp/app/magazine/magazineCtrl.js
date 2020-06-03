(function(){
    "use strict";
    angular.module("DppApp")
        .controller("MagazineCtrl",  ['$http', MagazineCtrl]);

    //MagazineCtrl.$inject = ["NgTableParams"];

    function MagazineCtrl($http){
      var self = this;
      // recuperamos el get del servidor
      $http.get("/api/magazine/list/")
        .then(
            function(response){
              self.diarios = response.data;
              console.log(self.diarios);
            }
        );

      self.tipo_diario = function(variable){
        console.log(variable);
        if (variable=='Diario') {
          return true;
        }
        else {
          return false;
        }
      }
      self.tipo_producto = function(variable){
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

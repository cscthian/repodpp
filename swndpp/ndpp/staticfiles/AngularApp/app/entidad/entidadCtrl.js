(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("EntidadCtrl",  ['$http', EntidadCtrl]);

    //MagazineCtrl.$inject = ["NgTableParams"];

    function EntidadCtrl($http){
      var vm = this;
      // recuperamos el get del servidor
      $http.get("/api/vendors")
        .then(
            function(response){
              vm.canillas = response.data;
            }
        );
    }
}())

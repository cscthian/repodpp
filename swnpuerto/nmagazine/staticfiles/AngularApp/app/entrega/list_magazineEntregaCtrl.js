(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("ListMagazineEntregaCtrl", ['$http','ngToast', ListMagazineEntregaCtrl]);

    function ListMagazineEntregaCtrl($http, ngToast){
        var vm = this;
        //inicializamos la lista de guias
        $http.get("/api/guide-detalle/list-asignar/")
          .then(function(response){
              console.log('cons de diarios');
              vm.magazins = response.data;
              console.log(response);
          }
        );
  }
}());

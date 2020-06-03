(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("EmitidosCtrl", ['$http','ngToast', EmitidosCtrl]);

    function EmitidosCtrl($http, ngToast){
        var vm = this;

        vm.cargar_boletas = function(){
            var d = new Date(vm.fecha1)
            var date1 = d.getDate() + "-" + (d.getMonth()+1) + "-" + d.getFullYear();
            var d2 = new Date(vm.fecha2)
            var date2 = d2.getDate() + "-" + (d2.getMonth()+1) + "-" + d2.getFullYear();
            //inicializamos la lista de guias
            $http.get("/api/boleta/emitidos/"+date1+"/"+date2+"/")
              .then(function(response){
                vm.boletas = response.data;
              }
            );
        }
  }
}());

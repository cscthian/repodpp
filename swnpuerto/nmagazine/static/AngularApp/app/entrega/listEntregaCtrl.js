(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("EntregaListCtrl", ['$http','ngToast', EntregaListCtrl]);

    function EntregaListCtrl($http, ngToast){
        var vm = this;

        vm.cargar_asignaciones = function(){
          var date1,date2;
          if ((vm.fecha2 == null) && (vm.fecha1 == null)) {
            var date = new Date();
            var dat1 = new Date();
            dat1 = new Date(dat1.setDate(dat1.getDate() + (-7)));

            date2 = date.getFullYear() + "-" + (date.getMonth()+1) + "-" + (date.getDate());
            date1 = dat1.getFullYear() + "-" + (dat1.getMonth()+1) + "-" + (dat1.getDate());
          }
          else {
            var d1 = new Date(vm.fecha1)
            var d2 = new Date(vm.fecha2)
            date1 = d1.getFullYear() + "-" + (d1.getMonth()+1) + "-" + d1.getDate() ;
            date2 = d2.getFullYear() + "-" + (d2.getMonth()+1) + "-" + d2.getDate();
          }

          //inicializamos la lista de guias
          $http.get("/api/asignations/"+date1+"/"+date2+"/")
            .then(function(response){
              vm.asignations = response.data;
            }
          );
        }
  }
}());

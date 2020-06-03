(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("GuidesCulminedCtrl", ['$http','ngToast', GuidesCulminedCtrl]);

    function GuidesCulminedCtrl($http, ngToast){
        var vm = this;
        //inicializamos la lista de guias
        vm.cargar_guias = function(){
          var date1 = vm.fecha1.getFullYear()+ "-" + (vm.fecha1.getMonth()+1) + "-" + vm.fecha1.getDate();
          var date2 =  vm.fecha2.getFullYear() + "-" + (vm.fecha2.getMonth()+1) + "-" + vm.fecha2.getDate();
          $http.get("/api/guides/culmined/"+date1+"/"+date2+"/")
            .then(function(response){
              vm.guias = response.data;
            }
          );
        }
  }
}());

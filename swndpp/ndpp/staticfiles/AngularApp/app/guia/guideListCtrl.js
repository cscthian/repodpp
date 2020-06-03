(function(){
    "use strict";
    angular.module("DppApp")
        .controller("GuideListCtrl", ['$http', GuideListCtrl]);

    function GuideListCtrl($http){
        var vm = this;

        //filtramos por ragno de fechas
        vm.rango_fecha = function(){
            //realizamos la logica de filtro
            var d1 = new Date(vm.fecha1)
            var date1 = d1.getFullYear() + "-" + (d1.getMonth()+1) + "-" + d1.getDate();
            //
            var d2 = new Date(vm.fecha2)
            var date2 = d2.getFullYear() + "-" + (d2.getMonth()+1) + "-" + d2.getDate();
            //
            $http.get("/api/guides/"+date1+"/"+date2+"/")
              .then(function(response){
                  vm.guias = response.data;
              }
            );
        }
  }
}());

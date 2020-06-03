(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("ListGuideCtrl", ['$http','ngToast', GuideListCtrl]);

    function GuideListCtrl($http, ngToast){
        var vm = this;
        //funcionalidad tecla enter
        vm.enter = function(keyEvent) {
          if (keyEvent.which === 13){
              vm.buscar_guias();
          }
        }

        //recuperamos lista de guais
        vm.buscar_guias = function(){
          $http.get("/api/reportes/guia/lista/"+vm.numero+"/")
            .then(function(response){
                vm.guias = response.data;
            }
          );
        }

  }
}())

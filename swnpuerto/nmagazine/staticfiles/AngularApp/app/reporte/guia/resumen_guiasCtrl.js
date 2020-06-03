(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("ListGuideResumenCtrl", ['$http','ngToast', ListGuideResumenCtrl]);

    function ListGuideResumenCtrl($http, ngToast){
        var vm = this;
        vm.anulado = "";
        vm.devuelto = "";
        vm.asignado = "";
        vm.todo = false;
        //inicializamos la lista de guias

        vm.buscar_guias = function(){
          var d1 = new Date(vm.fecha1);
          var date1 = d1.getFullYear() + "-" + (d1.getMonth()+1) + "-" + d1.getDate();
          var d2 = new Date(vm.fecha2);
          var date2 = d2.getFullYear() + "-" + (d2.getMonth()+1) + "-" + d2.getDate();

          $http.get("/api/reportes/resumen-guia/"+date1+"/"+date2+"/")
            .then(function(response){
                vm.guias = response.data;
            }
          );
        }

        vm.reiniciar = function(){
            console.log(vm.todo);
            vm.anulado = false;
            vm.devuelto = false;
            vm.asignado = false;
            vm.anulado = "";
            vm.devuelto = "";
            vm.asignado = "";
        }
        //imprimir funcion
        vm.imprimir = function(){
          console.log(vm.count_reales);
          vm.printDiv('print-section');
          window.location.reload();
        }

        vm.printDiv = function(divName) {
          var printContents = document.getElementById(divName).innerHTML;
          var originalContents = document.body.innerHTML;
          document.body.innerHTML = printContents;
          window.print();
          document.body.innerHTML = originalContents;
        }

  }
}())

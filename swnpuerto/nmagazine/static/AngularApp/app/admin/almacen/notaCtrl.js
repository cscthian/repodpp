(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("NotaCtrl", ['$http', NotaCtrl]);

    function NotaCtrl($http, ngToast){
        var vm = this;

        //filtramos magazine day por numero e guia
        vm.listar_items = function(guia){
          $http.get("/api/nota/items/"+guia+'/')
            .then(function(response){
              vm.items = response.data;
            }
          )
          .catch(function(fallback) {
            console.log('no se encontro la guia');
          });
        }

        //consultamos la guia y el item
        vm.recuperar_objeto = function(magazine){
          for (var i = 0; i < vm.items.length; i++) {
            if (vm.items[i].pk == magazine) {
                vm.name = vm.items[i].name;
                vm.precio_guia = parseFloat(vm.items[i].precio_guia);
                vm.precio_venta = parseFloat(vm.items[i].precio_venta);
                vm.count = vm.items[i].count;
                var d = new Date(vm.items[i].date);
                vm.date = d.getDate() + "/" + (d.getMonth()+1) + "/" + d.getFullYear();
                console.log(vm.date);
            }
          }
        }
  }
}())

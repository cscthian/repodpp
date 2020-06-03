(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("ListLostCtrl",  ['$http','$window','ngToast', ListLostCtrl]);

    //MagazineCtrl.$inject = ["NgTableParams"];

    function ListLostCtrl($http, $window, ngToast){
      var vm = this;
      // recuperamos el get del servidor
      $http.get("/api/control/diarios/")
        .then(
            function(response){
              vm.losts = response.data;
            }
        );


      //calculamos el monto total
      vm.calcular_monto = function(modulo){
        var total = 0;
          for (var i = 0; i < vm.losts.length; i++) {
            if (modulo != ''){
              if (vm.losts[i].module == modulo) {
                  total = total + vm.losts[i].count*vm.losts[i].precio_venta;
              }
            }
            else {
              total = total + vm.losts[i].count*vm.losts[i].precio_venta;
            }
          }
          vm.monto = total;
      }

      //ceeramos la deudas
      vm.close_duda = function(){
        var modulo = {'module':vm.tipo};
        $http.post("/api/save/diairios/perdidos/close/", modulo)
            .success(function(res){
              if (res.id=='0') {
                ngToast.create(res.respuesta);
                $window.location.reload();
              }
              else {
                ngToast.create({
                  className: 'warning',
                  content: res.respuesta,
                });
              }
              //$location.href
            })
            .error(function(res){
              ngToast.create({
                className: 'warning',
                content: '<a href="#">x Error Revise los datos</a>',
              });
            });
      }
    }
}())

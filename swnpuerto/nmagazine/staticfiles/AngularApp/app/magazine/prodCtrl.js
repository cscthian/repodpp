(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("ProdCtrl",  ['$http', ProdCtrl]);

    //MagazineCtrl.$inject = ["NgTableParams"];

    function ProdCtrl($http){
      var vm = this;

      vm.recuperar_magazine = function(codigo){
        $http.get("/api/producto/retrive/"+codigo+"/")
          .then(
              function(response){
                var objeto = response.data;
                vm.precio_guia = parseFloat(objeto.precio_guia);
                vm.precio_tapa = parseFloat(objeto.precio_tapa);
                vm.precio_venta = parseFloat(objeto.precio_venta);
              }
          );
      }
      vm.cargar_porcentaje = function(tipo){
        vm.porcentaje = parseFloat(tipo);
      }

      vm.calcular_precio = function(porcentaje, precio){
        var res1 = precio - (parseFloat(porcentaje)/100)*precio;
        vm.precio_venta = res1;
        var res2 = (precio - ((parseFloat(porcentaje)+6)/100)*precio);
        vm.precio_guia = parseFloat(res2.toFixed(3));
      }

      //metodo que lista productos por cobrar
      vm.productos_por_cobrar = function(){
        var date;
        if (vm.fecha1 == null){
          var f = new Date();
          date = f.getDate() + "-" + (f.getMonth()+1) + "-" + f.getFullYear();
        }
        else {
          var f = new Date(vm.fecha1);
          date = f.getDate() + "-" + (f.getMonth()+1) + "-" + f.getFullYear();
        }
        $http.get("/api/productos/por-cobrar/"+date+"/")
          .then(
              function(response){
                vm.productos = response.data;
              }
          );
      }

    }
}())

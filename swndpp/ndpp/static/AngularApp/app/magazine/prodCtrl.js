(function(){
    "use strict";
    angular.module("DppApp")
        .controller("ProdCtrl",  ['$http', ProdCtrl]);

    //MagazineCtrl.$inject = ["NgTableParams"];

    function ProdCtrl($http){
      var self = this;

      self.recuperar_magazine = function(codigo){
        $http.get("/api/producto/retrive/"+codigo+"/")
          .then(
              function(response){
                var objeto = response.data;
                self.precio_guia = parseFloat(objeto.precio_guia);
                self.precio_tapa = parseFloat(objeto.precio_tapa);
                self.precio_venta = parseFloat(objeto.precio_venta);
              }
          );
      }
      self.cargar_porcentaje = function(tipo){
        self.porcentaje = parseFloat(tipo);
      }

      self.calcular_precio = function(porcentaje, precio){
        var res1 = precio - (parseFloat(porcentaje)/100)*precio;
        self.precio_venta = res1;
        var res2 = (precio - ((parseFloat(porcentaje)+6)/100)*precio);
        self.precio_guia = parseFloat(res2.toFixed(3));
      }

      //metodo que lista productos por cobrar
      self.productos_por_cobrar = function(){
        var date;
        if (self.fecha1 == null){
          var f = new Date();
          date = f.getDate() + "-" + (f.getMonth()+1) + "-" + f.getFullYear();
        }
        else {
          var f = new Date(self.fecha1);
          date = f.getDate() + "-" + (f.getMonth()+1) + "-" + f.getFullYear();
        }
        $http.get("/api/productos/por-cobrar/"+date+"/")
          .then(
              function(response){
                self.productos = response.data;
              }
          );
      }

    }
}())

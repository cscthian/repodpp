(function(){
    "use strict";
    angular.module("DppApp")
        .controller("CompraTotalCtrl", ['$http', CompraTotalCtrl]);

    function CompraTotalCtrl($http){
        var self = this;

        self.total = 0;

        $http.get("/api/provider")
          .then(function(response){
              self.providers = response.data;
          }
        );
        //
        //inicializamos la lista de departamentos
        $http.get("/api/departamento")
          .then(function(response){
              self.departamentos = response.data;
          }
        );
        self.cargar_consulta = function(){
          console.log('log de prueba');
          //
          $http.get("/api/reportes/ventas/compra-total/"+self.rs+"/"+self.departamento+"/"+self.proveedor+"/")
            .then(function(response){
                self.consulta = response.data
                self.calcular_total();
            }
          );
        };
        //
        self.calcular_total = function() {
          self.total = 0;
          for (var i = 0; i < self.consulta.length; i++) {
            self.total = self.total + self.consulta[i].subtotal;
          }
          self.total = self.total.toFixed(3);
        }
  }
}());

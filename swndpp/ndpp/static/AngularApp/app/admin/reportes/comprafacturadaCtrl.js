(function(){
    "use strict";
    angular.module("DppApp")
        .controller("CompraFacturadaCtrl", ['$http', CompraFacturadaCtrl]);

    function CompraFacturadaCtrl($http){
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
          if (self.date) {
            var d = new Date(self.date)
            var date = d.getFullYear() + "-" + (d.getMonth()+1) + "-" + d.getDate();
            //
            $http.get("/api/reportes/ventas/compra-facturada/"+self.proveedor+"/"+self.departamento+"/"+self.rs+"/"+date+"/")
              .then(function(response){
                  self.consulta = response.data
                  self.calcular_total();
                  self.calcular_montos_por_guia();
              }
            );
          }
        };
        //metodo para reagrupar
        self.calcular_montos_por_guia = function() {
          var monto_aux = 0;
          for (var i = 0; i < self.consulta.length; i++) {
            var obj = self.consulta[i];
            var guia;
            if (i == 0) {
              guia = self.consulta[i].guia;
              monto_aux = self.consulta[i].subtotal;
            }
            else {
              if (obj.guia == self.consulta[i-1].guia) {
                // acumulamos monto
                monto_aux = monto_aux + obj.subtotal;
              }
              else {
                self.consulta[i-1].monto = monto_aux.toFixed(3);
                monto_aux = self.consulta[i].subtotal;
              }
            }
            //si ya estamos al final
            if (i == (self.consulta.length - 1)) {
              self.consulta[i].monto = monto_aux.toFixed(3);
            }
          }
        }
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

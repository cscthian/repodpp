(function(){
    "use strict";
    angular.module("DppApp")
        .controller("FaltanteCtrl", ['$http','$window', FaltanteCtrl]);

    function FaltanteCtrl($http,$window){
        var self = this;

        //
        self.consulta = []
        //
        self.items = [];
        //
        self.total = 0;
        //
        self.cargar_items = function(){
          self.items = [];
          //
          self.total = 0;
          //
          $http.get("/api/montos-faltantes/")
            .then(function(response){
                self.consulta = response.data
                for (var i = 0; i < self.consulta.length; i++) {
                  self.consulta[i].monto_deuda = (self.consulta[i].monto_factura - self.consulta[i].monto_real).toFixed(3);
                  self.items.push(self.consulta[i])
                }
                self.calcular_montos();
            }
          );
        }

        //funcion para calcuar montos
        self.calcular_montos = function() {
          self.total = 0;
          var total = 0;
          for (var i = 0; i < self.items.length; i++) {
            total = total + parseFloat(self.items[i].monto_deuda);
          }
          self.total = total.toFixed(3);
        }

        //funcion para filtrar datos por responsabilidad
        self.filtrar_responsabilidad = function (flat) {
          self.items = [];
          if (flat == '0') {
            for (var i = 0; i < self.consulta.length; i++) {
              if (self.consulta[i].responsabilidad == 'Admin') {
                self.items.push(self.consulta[i]);
              }
            }
          } else if (flat == '1') {
            for (var i = 0; i < self.consulta.length; i++) {
              if (self.consulta[i].responsabilidad == 'Almacen') {
                self.items.push(self.consulta[i]);
              }
            }
          } else if (flat == '2') {
            for (var i = 0; i < self.consulta.length; i++) {
              if (self.consulta[i].responsabilidad == 'Caja') {
                self.items.push(self.consulta[i]);
              }
            }
          } else {
            for (var i = 0; i < self.consulta.length; i++) {
              if (self.consulta[i].responsabilidad == 'Otros') {
                self.items.push(self.consulta[i]);
              }
            }
          }
          self.calcular_montos();
        }

        //enviar items
        self.saldar_perdidas = function () {
          //json a enviar
          var json = [];
          //
          for (var i = 0; i < self.items.length; i++) {
            //auxiliar
            var i = {
              'pk':self.items[i].pk
            }
            json.push(i);
          }
          //
          $http.post("/api/save/montos-faltantes/", json)
              .success(function(res){
                console.log(res.data);
                $window.location.reload();
              })
              .error(function(res){
                console.log(res.data);
              });
          }
  }
}());

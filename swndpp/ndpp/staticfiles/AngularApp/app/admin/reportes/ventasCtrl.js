(function(){
    "use strict";
    angular.module("DppApp")
        .controller("VentasCtrl", ['$http', VentasCtrl]);

    function VentasCtrl($http){
        var self = this;

        self.items = [];

        self.total = 0;
        self.descuento = 6;

        self.cargar_items = function(){
          self.descuento = 6;
          //
          var d = new Date(self.fecha_inicio)
          var date = d.getFullYear() + "-" + (d.getMonth()+1) + "-" + d.getDate();
          //
          var d2 = new Date(self.fecha_fin)
          var date2 = d2.getFullYear() + "-" + (d2.getMonth()+1) + "-" + d2.getDate();
          //
          self.items = [];
          //
          $http.get("/api/cuadre-ventas/"+date+"/"+date2+"/")
            .then(function(response){
                self.items = response.data
                self.calcular_montos();
            }
          );
        }

        self.calcular_montos = function(){
            self.total = 0;
            //primero verificamos el tipo de razon social
            for (var i = 0; i < self.items.length; i++) {
              self.total = parseFloat(self.total) + parseFloat(self.items[i].total);
              self.total = self.total.toFixed(3);
            }
            //aplicamos el descuento
            var dto;
            if (self.descuento == '') {
              dto = 0;
            }
            dto = parseFloat(self.descuento);

            self.total = parseFloat(self.total) - (parseFloat(self.total)*(dto/100))
            self.total = self.total.toFixed(3);
        }


  }
}());

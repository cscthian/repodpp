(function(){
    "use strict";
    angular.module("DppApp")
        .controller("FacturaCtrl", ['$http','$window', FacturaCtrl]);

    function FacturaCtrl($http,$window){
        var self = this;

        //variable total
        self.monto_total = 0;
        self.monto_real = 0;
        //filtramos por ragno de fechas
        self.listar_factura = function(){
            //
            $http.get("/api/factura/list/")
              .then(function(response){
                  self.facturas = response.data;
                  self.verificar_nota_credito();
              }
            );
        }

        // verificamos si la nota de credito se aproxima
        self.verificar_nota_credito = function() {
          for (var i = 0; i < self.facturas.length; i++) {
            var aux = parseFloat(self.facturas[i].amount) - (parseFloat(self.facturas[i].monto_factura) + parseFloat(self.facturas[i].amount_nota))
            console.log(aux);
            if (aux < 1) {
              self.facturas[i].correcto = true;
            }
          }
        }

        //calculamos monto de los selccionados
        self.recalcular_monto = function(){
          self.monto_total = 0;
          self.monto_real = 0;
          for (var i = 0; i < self.facturas.length; i++) {
            console.log(self.facturas[i]);
            if (self.facturas[i].state == true) {
              self.monto_total = parseFloat(self.monto_total) + parseFloat(self.facturas[i].amount);
              self.monto_real = parseFloat(self.monto_real) + parseFloat(self.facturas[i].monto_factura);
            }
          }
          self.monto_total = self.monto_total.toFixed(4);
          self.monto_real = self.monto_real.toFixed(4);
        }

        //registramos los pagos
        self.registrar_pago = function(){
          var datos = [];
          var d = new Date(self.date_pago);
          var date = d.getFullYear() + "-" + (d.getMonth()+1) + "-" + d.getDate();
          for (var i = 0; i < self.facturas.length; i++) {
            if (self.facturas[i].state == true) {
              var objeto_factura= {
                'factura':self.facturas[i].number,
                'codigo_pago':self.codigo_pago,
                'responsabilidad':self.facturas[i].responsabilidad,
                'date_pago':date,
                'monto_real':self.facturas[i].monto_factura
              };
              datos.push(objeto_factura);
            }
          }
          //
          console.log(datos);
          //
          $http.post("/api/save/pago-factura/", datos)
                .success(function(res){
                  if (res.id == '0') {
                    console.log(res);
                    $window.location.reload();
                  }
                  else {
                    console.log(res);
                  }
          })
        }
  }
}());

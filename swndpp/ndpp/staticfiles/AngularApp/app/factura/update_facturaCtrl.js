(function(){
    "use strict";
    angular.module("DppApp")
        .controller("FacturaUpdateCtrl", ['$http','$window', FacturaUpdateCtrl]);

    function FacturaUpdateCtrl($http,$window){
        var self = this;

        //variable total
        self.monto_seleccion = 0;
        self.count_seleccion = 0;
        //
        self.monto_items_voucher = 0;
        self.count_items_voucher = 0;
        //
        self.monto_add = 0;
        self.count_add = 0;

        //inicializamos la lista de proveedores
        $http.get("/api/provider")
          .then(function(response){
              self.providers = response.data;
          }
        );


        //inicializamos la lista de departamentos
        $http.get("/api/departamento")
          .then(function(response){
              self.departamentos = response.data;
          }
        );

        // cargamos los items agregados a la fatura
        self.items_agregado_factura = function(voucher){
          $http.get("/api/voucher-guide-items/"+voucher+"/")
            .then(function(response){
                self.items_agregados = response.data;
                self.calcular_montos_items_voucher();
            }
          );
        }

        self.calcular_montos_items_voucher = function(){
          self.monto_items_voucher = 0;
          self.count_items_voucher = 0;
          for (var i = 0; i < self.items_agregados.length; i++) {
            //se realiza la suma
            self.count_items_voucher = self.count_items_voucher + self.items_agregados[i].count;
            self.monto_items_voucher = self.monto_items_voucher + (self.items_agregados[i].precio_guia*self.items_agregados[i].count);
          }
          self.monto_items_voucher = self.monto_items_voucher.toFixed(3);
        }

        //filtramos por ragno de fechas
        self.listar_items_date = function(){
            self.items = [];
            //cambiamos formato de fecha
            var d = new Date(self.fecha);
            var date = d.getFullYear() + "-" + (d.getMonth()+1) + "-" + d.getDate();
            $http.get("/api/items-guide/"+date+"/")
              .then(function(response){
                  self.items = response.data;
                  self.calcular_montos_seleccion();
              }
            );
        }

        //funcion para calcular montos
        self.calcular_montos_seleccion = function(){
          self.monto_seleccion = 0;
          self.count_seleccion = 0;
          for (var i = 0; i < self.items.length; i++) {
            if (self.items[i].state == true) {
              //se realiza la suma
              self.count_seleccion = self.count_seleccion + self.items[i].count;
              self.monto_seleccion = self.monto_seleccion + (self.items[i].precio_guia*self.items[i].count);
            }
          }
          self.monto_seleccion = self.monto_seleccion.toFixed(3);
        }

        //
        self.limpiar_seleccion = function(){
          self.monto_seleccion = 0;
          self.count_seleccion = 0;
          for (var i = 0; i < self.items.length; i++) {
            self.items[i].state = false;
          }
        }

        //funcion que recalcula valores para filtro por departamento
        self.seleccionar_by_departamento = function(){
          for (var i = 0; i < self.items.length; i++) {
            if (self.items[i].departamento == self.departamento ) {
              self.items[i].state = true;
            }
            else {
              self.items[i].state = false;
            }
          }
          self.calcular_montos_seleccion();
        }

        //funcion que recalcula valores para filtro por proveedore
        self.seleccionar_by_provider = function(){
          for (var i = 0; i < self.items.length; i++) {
            if (self.items[i].provider == self.provider ) {
              self.items[i].state = true;
            }
            else {
              self.items[i].state = false;
            }
          }
          self.calcular_montos_seleccion();
        }

        //funcion que agregar item a factura
        self.agregar_item = function(voucher){
          self.calcular_montos_seleccion();
          //generamos el detalle a guardar
          var json = [];
          for (var i = 0; i < self.items.length; i++) {
            if (self.items[i].state == true) {
              var detail_voucher = {
                'voucher':voucher,
                'dettail_guide':self.items[i].id
              };
              json.push(detail_voucher);
            }
          }
          console.log(json);
          //enviamos los selccionados a registro
          $http.post("/api/save-guide/voucher/", json)
              .success(function(res){
                $http.get("/api/voucher-guide-items/"+voucher+"/")
                  .then(function(response){
                      self.items_agregados = response.data;
                      self.calcular_montos_items_voucher();
                  }
                );
              })
              .error(function(res){
                console.log('error no se pudo agregar');
              });
        }

        //metodo para eliminar un item de lista agregados
        //funcion que agregar item a factura
        self.delete_item = function(detail_voucher, voucher){
          //generamos el detalle a guardar
          var json = {
            'voucher':detail_voucher
          };
          console.log(json);
          //enviamos los selccionados a registro
          $http.post("/api/delete-guide/voucher/", json)
              .success(function(res){
                self.items_agregado_factura(voucher);
                self.calcular_montos_items_voucher();
              })
              .error(function(res){
                console.log('error no se pudo agregar');
              });
          //
        }
  }
}());

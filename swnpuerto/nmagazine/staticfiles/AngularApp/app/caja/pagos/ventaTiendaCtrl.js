(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("VentaTiendaCtrl",  ['$http','uiGridConstants','ngToast','$window',VentaTiendaCtrl]);

    function VentaTiendaCtrl($http,uiGridConstants,ngToast,$window,hotkeys){
      var vm = this;

      vm.valido = false;
      vm.productos_en_venta = [];

      vm.cantidad = 1;

      vm.sub_total = 0.00;

      $http.get("/api/pagos/lista-productos-venta/")
        .then(function(response){
            vm.productos = response.data;
        }
      );

      vm.enter = function(keyEvent) {
        if (keyEvent.which === 13){
            vm.agregar_producto(vm.codigo);
        }
      }

      //metodo para quitar un producto por pk
      vm.quitar_producto = function(codigo){
        console.log('---'+codigo);
        //recorremps el lista de prod
        var index = -1;
        for (var i = 0; i < vm.productos_en_venta.length; i++) {
          if (vm.productos_en_venta[i].pk == codigo) {
            index = i;
          }
        }
        //eliminamos el producto
        vm.productos_en_venta.splice(index,1);
        //sumamos el total para calcular sub total
        vm.sub_total = 0;
        for (var i = 0; i < vm.productos_en_venta.length; i++) {
          vm.sub_total = vm.sub_total + vm.productos_en_venta[i].total;
        }
      }
      //metodo que agrega productos
      vm.agregar_producto = function(){
        vm.valido = false;
        //recuperamos el objeto
        console.log('entro agregar producto');
          $http.get("/api/detail_guide/retrive/"+vm.producto+"/")
            .then(function(response){
                vm.productos_en_venta.push(
                  {
                    pk:response.data.pk,
                    magazine:response.data.magazine_day,
                    count:vm.cantidad,
                    precio_unitario:response.data.precio_unitario,
                    total:vm.cantidad*response.data.precio_unitario,
                  }
                );
                //sumamos el total para calcular sub total
                vm.sub_total = vm.sub_total + vm.cantidad*response.data.precio_unitario;
            }
          );
      }
      //metodo para calcular el vuelto
      vm.calcular_vuelto = function(){
        vm.vuelto = vm.pago_con - vm.cobrar;
        vm.vuelto = vm.vuelto.toFixed(3);
      }

      vm.validar_data = function(){
        if ((vm.productos_en_venta.length > 0) && (vm.sub_total > 0)) {
          console.log(vm.productos_en_venta.length );
          console.log(vm.sub_total);
          return true;
        }
        else {
          console.log('Error');
          return false;
        }
      }

      //metodo que crea datos
      vm.datos_enviar = function(){
        var datos = [];
        for (var i = 0; i < vm.productos_en_venta.length; i++) {
          datos.push({
              pk:vm.productos_en_venta[i].pk,
              count:vm.productos_en_venta[i].count,
          });
        }
        return datos;
      }

      //metodo para enviar los datos validados
      vm.enviar_data = function(){
        vm.valido = false;
        if (vm.validar_data()) {
          //creamos el json a enviar
          var datos = vm.datos_enviar();
          $http.post("/api/ventas/save/",datos)
              .success(function(res){
                //console.log(res);
                ngToast.create('se guardo el Pago correctamente');
                window.location.href = '/caja/cobros/venta-tienda/';
              })
              .catch(function(fallback) {
                ngToast.create({
                  className: 'danger',
                  content: "Error, Verifique que los datos sean Numeros",
                });
              });
        }
        else {
          vm.valido = true;
          vm.mensaje = 'Error Verifique los Datos'
          ngToast.create({
            className: 'danger',
            content: "Error, Verifique que los datos sean Numeros",
          });
        }

      }

    }
}())

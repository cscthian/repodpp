(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("DetalleHistoryCtrl",  ['$http', '$window','ngToast',DetalleHistoryCtrl]);

    function DetalleHistoryCtrl($http,$window,ngToast){
      var vm = this;
      //funcion que consulta guias en rango de fechas
      vm.cargar_detalle = function(parametro){

        //inicializamos monto cobrado
        vm.monto_cobrado = 0;
        vm.total_devuelto = 0;
        $http.get("/api/reportes/detalle-guia/"+parametro+'/')
          .then(function(response){
            vm.historial = response.data;
          }
        )
        .catch(function(fallback) {
          console.log('error');
        });
    }

    //funcion para enviar datos al servidor
    vm.enviar_data = function(){
      //contruimos un json a enviar al servidor
      var obj = vm.count_reales.item;
      var arry = Object.keys(obj).map(function (key) { return obj[key]; });
      //recorremos el json y generamos un nuevo son
      var data_real = [];
      var index = vm.historial.length-1;
      var i = 0;
      while (index >= 0) {
        if (!isNaN(arry[i])) {
          data_real.push(
            {
              'pk':vm.historial[index].pk,
              'count':vm.historial[index].count_almacen - arry[i],
            }
          );
          i = i + 1;
          index = index - 1
        }
        else {
          i = i + 1;
          index = index - 1
          ngToast.create({
            className: 'warning',
            content: 'Ingrese un Numeros Validos',
          });
        }
      }
      console.log(data_real);
      $http.post("/api/reporte/guia/count-real/save/", data_real)
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

    //imprimir funcion
    vm.imprimir = function(){
      console.log(vm.count_reales);
      vm.printDiv('print-section');
      window.location.reload();
    }

    vm.printDiv = function(divName) {
      var printContents = document.getElementById(divName).innerHTML;
      var originalContents = document.body.innerHTML;
      document.body.innerHTML = printContents;
      window.print();
      document.body.innerHTML = originalContents;
    }
    };
}())

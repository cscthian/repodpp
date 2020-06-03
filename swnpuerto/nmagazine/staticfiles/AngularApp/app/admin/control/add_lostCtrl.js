(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("AddLostCtrl", ['$http','$window','ngToast', AddLostCtrl]);

    function AddLostCtrl($http, $window, ngToast){
        var vm = this;

        //inicializamos variables globales
        vm.choices = [{id:'choice1'},{id:'choice2'}];
        vm.buscar = [{id:'buscar1'},{id:'buscar2'}];
        vm.cantidad = [{id:0},{id:1}];

        //inicializamos json Guia
        vm.lost = {};

        //inicializamos los valores de dairios desde el servidor
        $http.get("/api/guide-detalle/sin-culminar/")
          .then(function(response){
              vm.diarios = response.data;
          }
        );

        //metodo que agraga campos dinamicamente
        vm.addNewChoice = function(){
            var newItemNo = vm.cantidad.length;
            vm.choices.push({'id':'choice'+newItemNo});
            vm.buscar.push({'id':'buscar'+newItemNo})
            vm.cantidad.push({'id':newItemNo});
        };


        //metodo que elimina un formulario
        vm.removeChoice = function() {
            var lastItem = vm.cantidad.length-1;
            vm.choices.splice(lastItem);
            vm.buscar.splice(lastItem);
            vm.cantidad.splice(lastItem);
        };


        //funcion para enviar datos
        vm.enviar = function(){
            var lost_magazine = [];
            for (var i = 0; i < vm.cantidad.length; i++) {

                //creamos el json
                var row = {
                    module:vm.module,
                    detail_guide:vm.prod.item[i],
                    count:vm.count.item[i],
                    description:vm.descripcion,
                };
                lost_magazine.push(row);
            }

            $http.post("/api/save/diairios/perdidos/", lost_magazine)
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
        };
  }
}());

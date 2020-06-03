(function(){
    "use strict";
    angular.module("DppApp")
        .controller("GuideUpdateCtrl", ['$http', GuideUpdateCtrl]);

    function GuideUpdateCtrl($http){
        var vm = this;

        //inicializamos los valores de dairios desde el servidor
        $http.get("/api/magazine")
          .then(function(response){
              vm.diarios = response.data;
          }
        );


        //inicializamos variables
        vm.lista_items = function(pk){
          $http.get("/api/update/guide/"+pk+"/")
            .then(function(response){
                vm.guide_items = response.data;
            }
          );
        };


      //UPDATE-metodo para agregar items a auna guia
        vm.add_items = function(object_guide){
          var items_guide ={
                'pk':object_guide,
                'magazine_day':vm.guide_day,
                'count':vm.guide_cantidad,
                'guide':object_guide,
          };
          //agregamos al servidor
          $http.post("/api/save/detail/guide/", items_guide)
              .success(function(res){
                console.log('correcto');
              });
          //re-inicializamos los valores
          vm.lista_items(object_guide);
          console.log('arry not'+vm.guide_items+'not fount');
          vm.guide_day = null;
          vm.guide_cantidad = null;
          vm.lista_items(object_guide);
        };


      //UPDATE -metodo para eliminar un item
        vm.delete_items = function(guia,objeto){
          $http.post("/api/guide/detail/delete/"+guia+"/", objeto)
              .success(function(res){
                console.log('correcto');
              });
          vm.lista_items(objeto);
          vm.guide_day = null;
          vm.guide_cantidad = null;
          vm.lista_items(objeto);
        };


      //UPDATE input editable
        vm.editable = function(indice,pk){
            console.log(vm.day_cantidad);
        }


      //UPDATE - METODO PARA actualizar un registro de guia detalle
        vm.update_items = function(){
          console.log('actualizado');
        }


        //filtramos por ragno de fechas
        vm.rango_fecha = function(){
            if (vm.fecha1==null) {
              vm.fecha1 = '2015/01/01';
            }
            if (vm.fecha2==null) {
              vm.fecha2 = new Date();
            }
            //realizamos la logica de filtro
            vm.guias = [];
            for (var i = 0; i < vm.guides.length; i++) {
              var fecha = new Date(vm.guides[i].created)
              if (fecha<=vm.fecha2 && fecha >= vm.fecha1) {
                vm.guias.push(vm.guides[i]);
              }
              else {
                console.log('False');
              }
            }
        }
  }
}());

(function(){
    "use strict";
    angular.module("DppApp")
        .controller("GuideCtrl", ['$http','$window', GuideCtrl]);

    function GuideCtrl($http, $window){
        var self = this;

        //inicializamos variables globales
        self.choices = [{id:'choice1'},{id:'choice2'}];
        self.buscar = [{id:'buscar1'},{id:'buscar2'}];
        self.cantidad = [{id:0},{id:1}];
        self.devoluciones = [{id:0},{id:1}];

        self.msj = "";
        self.bloqueo = false;

        //inicializamos json Guia
        self.guide = {};
        self.guide.asignar = false;


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


        //inicializamos la lista de agentes
        self.cagar_agentes = function(){
          $http.get("/api/vendors")
            .then(function(response){
                self.agentes = response.data;
                console.log(self.agentes);
              }
            );
        }


        //inicializamos los valores de dairios desde el servidor
        $http.get("/api/magazine-day/list/")
          .then(function(response){
              self.diarios = response.data;
          }
        );

        //declaramos array que enviaremos para diarios y cantidad
        //metodo que agraga campos dinamicamente
        self.addNewChoice = function(){
            var newItemNo = self.cantidad.length;
            self.choices.push({'id':'choice'+newItemNo});
            self.buscar.push({'id':'buscar'+newItemNo})
            self.cantidad.push({'id':newItemNo});
            self.devoluciones.push({'id':'dev'+newItemNo});
        };


        //metodo que elimina un formulario
        self.removeChoice = function() {
            var lastItem = self.cantidad.length-1;
            self.choices.splice(lastItem);
            self.buscar.splice(lastItem);
            self.cantidad.splice(lastItem);
            self.devoluciones.splice(lastItem);
        };


        //funcion para enviar datos
        self.enviar = function(){
          if (self.validations()){
            self.bloqueo = true;
            self.msj = "";
            //ingresamos las cantidades no eliminadas al json
            var counts_magazines = [];
            var prod_magazines = []
            var devolucion = []
            for (var i = 0; i < self.cantidad.length; i++) {
                counts_magazines.push(self.count.item[i]);
                prod_magazines.push(self.prod.item[i]);
                devolucion.push(self.dev.item[i]);
            }
            //self.guide.provider = self.proveedor
            self.guide.counts = counts_magazines;
            self.guide.prods = prod_magazines;
            self.guide.devolucion = devolucion;
            //validamos fecha
            var date_cobranza = new Date(self.date_cobranza)
            var date = new Date(self.date)
            self.guide.date_cobranza = date_cobranza.getFullYear()+'-'+ (date_cobranza.getMonth()+1) +'-'+ date_cobranza.getDate();
            self.guide.date = date.getFullYear()+'-'+ (date.getMonth()+1) +'-'+ date.getDate();

            $http.post("/api/save/guide/add/", self.guide)
                .success(function(res){
                  if (res.id=='0') {
                    console.log('agregado correctamente');
                    window.location.href = '/guia-registrar/';
                  }
                  else {
                    console.log('Erro, no se pudo agregar');
                  }
                  //$location.href
                })
                .error(function(res){
                  self.msj = "ERROR VERIFIQUE QUE LOS DATOS SEAN CORRECTOS";
                  console.log('error no se pudo agregar');
                });
            }
        };

      //========validations===========
      self.validations = function(){
        if ((self.guide.addressee=='')||(self.guide.number=='')||(self.guide.provider=='')||(self.guide.agente=='')) {
          self.msj == 'Por favor ingrese todos los datos'
          return false;
        }
        else {
          self.msj=='';
          return true;
        }
      }
  }
}());

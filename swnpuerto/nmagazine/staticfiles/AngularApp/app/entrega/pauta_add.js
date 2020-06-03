(function(){
    "use strict";
    angular.module("MagazineApp")
        .controller("PautaAddCtrl",  ['$http','uiGridConstants','ngToast', PautaAddCtrl]);

    //MagazineCtrl.$inject = ["NgTableParams"];

    function PautaAddCtrl($http,uiGridConstants,ngToast){
      var vm = this;
      vm.date = new Date();

      vm.total = 0;
      vm.por_entregar = 0;
      vm.resto = 0;

      vm.progres = "0%";
      vm.is_error = false;
      vm.is_warning = false;
      vm.is_good = false;

      vm.gridOptions = {
        enableFiltering: true,
        infiniteScrollRowsFromEnd: 40,
        infiniteScrollUp: true,
        columnDefs : [
          {
            name: 'cod',
            enableColumnMenu: false,
            sort: {
              direction: uiGridConstants.ASC,
              priority: 0
            },
            displayName: 'Codigo',
            enableCellEdit: false,
            type: 'number',
            width: 100
          },
          {
            name: 'name',
            displayName: 'Nombres',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false
          },
          {
            name: 'tipo',
            displayName: 'Tipo',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false
          },
          {
            name: 'count',
            displayName: 'Cantidad',
            enableColumnMenu: false,
            enableCellEditOnFocus:false
          },
        ],
        //personalizamos el pdf
        enableGridMenu: true,
        enableSelectAll: false,
        exporterMenuCsv: false,
        exporterMenuPdf: false,
        exporterPdfDefaultStyle: {fontSize: 9},
        exporterPdfTableStyle: {margin: [5, 5, 5, 5]},
        exporterPdfTableHeaderStyle: {fontSize: 10, bold: true, italics: true, color: 'blue'},
        exporterPdfHeader: {
            text: "DPP PAUATA DE ENTREGA PRODUCTOS: "+vm.diario, style: 'headerStyle',
        },
        exporterPdfFooter: function ( currentPage, pageCount ) {
          return { text: currentPage.toString() + ' de ' + pageCount.toString(), style: 'footerStyle' };
        },
        exporterPdfCustomFormatter: function ( docDefinition ) {
          docDefinition.styles.headerStyle = { fontSize: 15, bold: true, margin: [50, 20, 20, 20] };
          docDefinition.styles.footerStyle = { fontSize: 10, bold: true };
          return docDefinition;
        },
        exporterPdfOrientation: 'portrait',
        exporterPdfPageSize: 'LETTER',
        exporterPdfMaxGridWidth: 500,
      };

      //cargamos la lista de diairos
      $http.get("/api/guide-detalle/lista-tipo/1/")
        .then(function(response){
            vm.diarios = response.data;
        }
      );

      //sugerimos pauta de otro producto
      vm.sugerir_pauta = function(total){
        vm.por_entregar = 0;
        vm.resto = 0;
        $http.get("/api/pauta/update/"+vm.diario_c+"/")
          .then(function(response){
              vm.gridOptions.data = response.data;
              console.log(vm.gridOptions.data);
              vm.total_entrega(total);
          }
        );
      }

      //funcion para generar un pauta en base a la BD
      vm.generar_pauta = function(codigo, total){
        vm.msj = '';
        vm.por_entregar = 0;
        vm.resto = 0;
        $http.get("/api/pautas/"+codigo)
          .then(function(response){
              vm.gridOptions.data = response.data;
              vm.diario = response.data[0].diario;
              vm.date = response.data[0].date;
              vm.total_entrega(total);
          }
        );
      }

      //funcion que recalcula un distirbucion en base a una cantidad
      // vm.recalcular_monto = function(){
      //   if (vm.count < 0){
      //     //quitamos
      //   }
      //   else {
      //     if (vm.count > 0) {
      //       //añadimos
      //     }
      //   }
      // }

      //funcion para clacular el total de entrega
      vm.total_entrega = function(total){
        for (var i = 0; i < vm.gridOptions.data.length; i++){
            vm.por_entregar = vm.por_entregar + parseInt(vm.gridOptions.data[i].count);
        }
        vm.resto = vm.total - vm.por_entregar;
        //seccion de validacion
        if (vm.por_entregar > vm.total) {
          vm.is_warning = false;
          vm.is_good = false
          vm.is_error = true;
        }
        else if (vm.por_entregar < vm.total) {
          vm.is_good = false
          vm.is_error = false;
          vm.is_warning = true;
        }
        else {
          vm.is_error = false;
          vm.is_warning = false;
          vm.is_good = true;
        }
        var porcentaje = (vm.por_entregar/vm.total)*100;
        vm.progres = porcentaje.toString()+"%";
      }

      //validamos que la guia sea ingresada
      vm.validar_datos = function(){
        if ((vm.guide == null) || (vm.guide.length == 0)) {
          return false;
        }
        else {
          return true;
        }
      }

      //cargamos la pauta diario
      vm.cargar_pauta = function(codigo, total){
        vm.msj = '';
        vm.por_entregar = 0;
        vm.resto = 0;
        vm.gridOptions.data = [];
        console.log('--------codigo-----------:'+codigo);
        $http.get("/api/pauta/update/"+codigo+"/")
          .then(function(response){
              vm.gridOptions.data = response.data;
              console.log(response.data);
              vm.diario = response.data[0].diario;
              vm.msj = response.data[0].mje;
              //recalculamos le valor de la barra
              vm.total_entrega(total);
          }
        );
      }

      vm.gridOptions.enableCellEditOnFocus = true;
      vm.currentFocused = "";

      vm.gridOptions.onRegisterApi = function(gridApi){
        vm.gridApi = gridApi;
        gridApi.edit.on.afterCellEdit(null,Validar);
            function Validar(){
              vm.por_entregar = 0;
              for (var i = 0; i < vm.gridOptions.data.length; i++){
                  vm.por_entregar = vm.por_entregar + parseInt(vm.gridOptions.data[i].count);
              }
              vm.resto = vm.total - vm.por_entregar;
              //seccion de validacion
              if (vm.por_entregar > vm.total) {
                vm.is_warning = false;
                vm.is_good = false
                vm.is_error = true;
              }
              else if (vm.por_entregar < vm.total) {
                vm.is_good = false
                vm.is_error = false;
                vm.is_warning = true;
              }
              else {
                vm.is_error = false;
                vm.is_warning = false;
                vm.is_good = true;
              }
              //actualizamos la barra de progreso
              var porcentaje = (vm.por_entregar/vm.total)*100;
              vm.progres = porcentaje.toString()+"%";

            }

      };

      vm.enviar = function(codigo){
        if (vm.validar_datos()) {
          //actualizamos el numero de guia
          for (var i = 0; i < vm.gridOptions.data.length; i++) {
            console.log(vm.guide);
            vm.gridOptions.data[i].guia = vm.guide;
            console.log('----'+vm.gridOptions.data[i].guia);
          }
          //enviamos lo datos
          $http.post("/api/pauta/save/"+codigo+"/", vm.gridOptions.data)
              .success(function(res){
                vm.gridOptions.data = [];
                vm.por_entregar = 0;
                vm.resto = 0;
                ngToast.create('se guardo la Pauta correctamente');
              });
        }
        else {
          ngToast.create({
            className: 'danger',
            content: '<p>Error: La guia no puede ser vacio</p>'
          })
        }
      };

      //funcion para dar de alta una pauta
      vm.habilitar_pauta = function(codigo){
        //creamo json a enviar
        if (vm.validar_datos()) {
          var data = {
            'guia':vm.guide,
            'enabled':true,
          }
          //enviamos la data
          $http.post("/api/pauta/habilitar/"+codigo+"/", data)
              .success(function(res){
                vm.gridOptions.data = [];
                vm.por_entregar = 0;
                vm.resto = 0;
                ngToast.create('Se Habilito la Pauta');
              });
        }
        else {
          ngToast.create({
            className: 'danger',
            content: '<p>Error: La guia no puede ser vacio</p>'
          })
        }
      }


      //funcion para deshabilitar una pauta
      vm.deshabilitar_pauta = function(codigo){
        //creamo json a enviar
        if (vm.validar_datos()) {
          var data = {
            'guia':vm.guide,
            'enabled':false,
          }
          //enviamos la data
          $http.post("/api/pauta/habilitar/"+codigo+"/", data)
              .success(function(res){
                vm.gridOptions.data = [];
                vm.por_entregar = 0;
                vm.resto = 0;
                ngToast.create('Se Deshabilitado la Pauta');
              });
        }
        else {
          ngToast.create({
            className: 'danger',
            content: '<p>Error: La guia no puede ser vacio</p>'
          })
        }
      }

      vm.limpiar = function(codigo, total){
        vm.msj = '';
        vm.por_entregar = 0;
        vm.resto = 0;
        vm.progres = "0%";

        $http.get("/api/pautas/"+codigo)
          .then(function(response){
              vm.gridOptions.data = response.data;
              vm.diario = response.data[0].diario;
              vm.date = response.data[0].date;
              vm.guide = response.data[0].guia;

              for (var i = 0; i < vm.gridOptions.data.length; i++) {
                  vm.gridOptions.data[i].count = 0;
              }
          }
        );
        vm.total = total;
      }

      vm.exportar = function(){
        vm.gridOptions.exporterPdfHeader = {
            text: "DPP REGISTRO DE PAUTA PRODUCTOS: "+vm.diario+" ("+vm.date+")", style: 'headerStyle',
        }
          vm.gridApi.exporter.pdfExport('all', 'selected');
      }
      //
      vm.exportarExcel = function(){
        vm.gridApi.exporter.csvExport('all', 'selected');
      }

    }
}())

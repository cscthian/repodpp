(function(){
    "use strict";
    angular.module("DppApp")
        .controller("CobrosCtrl",  ['$http','uiGridConstants','$window',CobrosCtrl]);

    function CobrosCtrl($http,uiGridConstants,$window,hotkeys){
      var self = this;

      self.class = "alert alert-success alert-sm";
      self.boleta = 0;
      self.pago = 0;
      self.deuda = 0;
      self.mensaje = '';
      self.alerta = '';
      self.vencido = false;
      self.not_orden = false;
      self.vendedor = "esperando nuevo agente..."


      self.enter = function(keyEvent) {
        if (keyEvent.which === 13){
            self.cargar_movimientos(self.codigo,self.usuario);
        }
      }

      //metodo para calcular el vuelto
      self.calcular_vuelto = function(){
        self.vuelto = self.pago_con - self.cobrar;
        self.vuelto = self.vuelto.toFixed(3);
      }

      self.gridOptions = {
        infiniteScrollRowsFromEnd: 10,
        infiniteScrollUp: true,
        columnDefs : [
          {
            name: 'tipo',
            enableColumnMenu: false,
            displayName: 'Tipo',
            enableCellEdit: false,
            sort: {
              direction: uiGridConstants.ASC,
              priority: 0
            },
            visible: false,
            width: 55
          },
          {
            name: 'vencido',
            cellClass: function(grid, row, col, rowRenderIndex, colRenderIndex) {
              if (grid.getCellValue(row,col).toLowerCase() === 'VENCIDO') {
                return 'blue';
              }
              else {
                return 'blue';
              }
            },
            enableColumnMenu: false,
            displayName: 'Estado',
            enableCellEdit: false,
            width: 70
          },
          {
            name: 'guide',
            cellClass:'black',
            enableColumnMenu: false,
            displayName: 'Guia',
            enableCellEdit: false,
            visible: false,
            width: 130
          },
          {
            name: 'date',
            cellClass:'black',
            enableColumnMenu: false,
            displayName: 'Fecha',
            enableCellEdit: false,
            sort: {
              direction: uiGridConstants.ASC,
              priority: 1
            },
            width: 130
          },
          {
            name: 'diario',
            enableColumnMenu: false,
            cellClass:'black',
            displayName: 'Diarios Productos',
            enableCellEdit: false,
            width: 250
          },
          {
            name: 'precio_venta',
            cellClass:'black',
            displayName: 'Precio',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 70
          },
          {
            name: 'amount',
            cellClass:'black',
            displayName: 'Monto',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 70
          },
          {
            name: 'entregado',
            cellClass:'black',
            displayName: 'Entregado',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false,
            width: 100
          },
          {
            name: 'devuelto',
            cellClass:'black',
            displayName: 'Devuelto',
            enableColumnMenu: false,
            enableCellEditOnFocus:false
          },
          {
            name: 'pagar',
            cellClass:'black',
            displayName: 'Pagar',
            enableColumnMenu: false,
            enableCellEditOnFocus:false
          },
          {
            name: 'deuda',
            cellClass:'black',
            displayName: 'A cuenta',
            enableColumnMenu: false,
            enableCellEdit: false,
            enableCellEditOnFocus:false
          },
        ],
        //personalizamos el pdf
        enableGridMenu: true,
        enableSelectAll: false,
        exporterMenuCsv: false,
        exporterMenuPdf: false,
        exporterPdfDefaultStyle: {fontSize: 9},
        exporterPdfTableStyle: {margin: [10, 30, 30, 30]},
        exporterPdfTableHeaderStyle: {fontSize: 10, bold: true, italics: true, color: 'red'},
        exporterPdfHeader: { text: "Deudas vendedor", style: 'headerStyle' },
        exporterPdfFooter: function ( currentPage, pageCount ) {
          return { text: currentPage.toString() + ' de ' + pageCount.toString(), style: 'footerStyle' };
        },
        exporterPdfCustomFormatter: function ( docDefinition ) {
          docDefinition.styles.headerStyle = { fontSize: 15, bold: true, margin: [250, 0, 20, 0] };
          docDefinition.styles.footerStyle = { fontSize: 10, bold: true };
          return docDefinition;
        },
        exporterPdfOrientation: 'portrait',
        exporterPdfPageSize: 'LETTER',
        exporterPdfMaxGridWidth: 500,
      };

      //cargamos la lista de canillas
      self.cargar_movimientos = function(codigo){
        //peticion get
        $http.get("/api/pagos/movimientos/"+codigo)
          .then(function(response){
              self.vendedor = response.data[0].canilla;
              self.boleta = response.data[0].boleta;

              self.gridOptions.data = response.data;
              self.fecha = new Date();

              self.pago = 0.00;
              self.deuda = 0.00;

              for (var i = 0; i < self.gridOptions.data.length; i++) {
                self.pago = self.pago + (self.gridOptions.data[i].pagar * self.gridOptions.data[i].precio_venta);
              }
              //redondeamos el resultado
              self.pago = self.pago.toFixed(3);
              //cargamos voucher por defecto
              self.cargar_voucher();
              self.cobrar = self.pago;
          }
        )
        .catch(function(fallback) {
          self.class = "alert";
          self.vendedor = "Error Verifique el Codigo, o el Cliente no tiene Deudas";
          self.gridOptions.data = [];
        });
      }

      self.gridOptions.enableCellEditOnFocus = true;

      self.currentFocused = "";

      self.gridOptions.onRegisterApi = function(gridApi){
        self.gridApi = gridApi;

        gridApi.edit.on.afterCellEdit(null,function(rowEntity, colDef, newValue, oldValue){
          self.mensaje = '';
          self.not_orden = false;
          self.alerta = '';
          if (colDef.name == "devuelto") {
              rowEntity.pagar = rowEntity.entregado - rowEntity.devuelto;
              rowEntity.deuda = rowEntity.entregado - rowEntity.devuelto - rowEntity.pagar;
              rowEntity.amount = rowEntity.pagar*rowEntity.precio_venta;
          }
          else {
              rowEntity.deuda = rowEntity.entregado - rowEntity.devuelto - rowEntity.pagar;
              rowEntity.amount = rowEntity.pagar*rowEntity.precio_venta;
          }

          self.pago = 0.00;
          self.deuda = 0.00;
          self.deudas = [];
          for (var i = 0; i < self.gridOptions.data.length; i++) {
            self.pago = self.pago + (self.gridOptions.data[i].pagar * self.gridOptions.data[i].precio_venta);
            if (self.gridOptions.data[i].tipo == 'Diario') {
              self.deuda = self.deuda + (self.gridOptions.data[i].deuda * self.gridOptions.data[i].precio_venta);
            }
            else {
              if ((self.usuario != '4')) {
                self.deuda = self.deuda + (self.gridOptions.data[i].deuda * self.gridOptions.data[i].precio_venta);
              }
              else {
                if (self.gridOptions.data[i].vencido == true) {
                  self.deuda = self.deuda + (self.gridOptions.data[i].deuda * self.gridOptions.data[i].precio_venta);
                }
              }
            }

            //generamos arreglo de vencido
            if ((self.gridOptions.data[i].deuda > 0)){
                self.deudas.push(
                  {
                    'name':'DEBE--'+self.gridOptions.data[i].diario+'('+self.gridOptions.data[i].deuda+')',
                  }
                )
            }
            //verificamos si numero negativo
            if (((self.pago < 0) || (self.deuda < 0)) && (self.gridOptions.data[i].precio_venta)>=0){
                self.mensaje = 'El PAGO o la DEUDA no pueden ser negativos';
                self.vencido = true;
            }

          }
          //redondeamos el resultado
          self.pago = self.pago.toFixed(3);
          self.deuda = self.deuda.toFixed(3)
          self.cargar_voucher();
          self.cobrar = self.pago;
        });
        //actualizamos voucher

      };

      self.validar_data = function(){
          var validado = true;
          self.error_msj = "";
          //validamos el grid
          if (isNaN(self.pago) || isNaN(self.deuda) || (self.date_operation==null) || (self.number_operation==null)){
              self.error_msj = "Error: revise los valores, no olvide ingresar numero de operacion y fecha de deposito";
              validado = false;
          }
          else {
            validado = true;
          }
          return validado;
      }

      self.enviar_data = function(){
        //completamos valor numero de operacion y fecha de operacion
        for (var i = 0; i < self.gridOptions.data.length; i++) {
          self.gridOptions.data[i].number_operation = self.number_operation;
          var date = new Date(self.date_operation)
          self.gridOptions.data[i].date_operation = date.getFullYear()+'-'+ (date.getMonth()+1) +'-'+ date.getDate();
        }
        if (self.validar_data()) {
          console.log(self.gridOptions.data);
          $http.post("/api/pagos/save/"+self.codCanilla+"/", self.gridOptions.data)
              .success(function(res){
                self.gridOptions.data = [];
                self.pago = 0.00;
                self.deuda = 0.00;
                self.deudas = [];
                self.por_cobrar = [];
                self.number_operation = "";
                self.date_operation = "";
              })
              .catch(function(fallback) {
                self.class = "alert alert-danger alert-sm";
                self.vendedor = "Nose Puede Gurdar La inforacion Verifique los datos";
              });
        }
        else {
          console.log('error');
        }

      }

    //poner todo en acuenta
    self.all_acount = function() {
      console.log('---');
      for (var i = 0; i < self.gridOptions.data.length; i++) {
        self.gridOptions.data[i].deuda = self.gridOptions.data[i].pagar;
        self.gridOptions.data[i].pagar = 0;
      }
    }

    //imprimir y guardar
    self.guardar_print = function(){
      if (self.validar_data()) {
        self.cargar_voucher();
        $http.post("/api/pagos/save/"+self.codCanilla+"/", self.gridOptions.data)
            .success(function(res){
              self.gridOptions.data = [];
              self.pago = 0.00;
              self.deuda = 0.00;
              self.deudas = [];
              self.por_cobrar = [];
              self.printDiv('print-section');
              console.log('se guardo correctamente');
              window.location.href = '/caja/cobros/cobrar/cobros';
            })
            .catch(function(fallback) {
              self.class = "alert alert-danger alert-sm";
              self.vendedor = "Nose Puede Gurdar La inforacion Verifique los datos";
            });;
      }
      else {
        console.log('error verifique los datos');
      }

    }

    //funcion rearma un texto
    self.cut_text = function(texto, tipo){
      var caracter = texto.split("");
      var first = '';
      var second = '-';
      for (var i = 0; i < caracter.length; i++) {
        if (tipo == 'Diario') {
          if (i < 6) {
            first = first + caracter[i];
          }
          else {
            if (caracter[i] == '[') {
              second = second + caracter[i+1] + caracter[i+2];
            }
          }
        }
        else {
          if (i < 6) {
            first = first + caracter[i];
          }
          else {
            if ((i+3)-caracter.length==1) {
              second = second + caracter[caracter.length-3] + caracter[caracter.length-2] + caracter[caracter.length-1];
            }
          }
        }

      }
      return first+second;
    }

    //cargar recibo por defecto
    self.cargar_voucher=function(){
      self.items = [];
      for (var i = 0; i < self.gridOptions.data.length; i++) {
          var sub_total = self.gridOptions.data[i].pagar*self.gridOptions.data[i].precio_venta;
          sub_total = sub_total.toFixed(2)
          if ((self.gridOptions.data[i].pagar > 0) ||(self.gridOptions.data[i].devuelto >0)) {
            var rows = {
              'item':self.cut_text(self.gridOptions.data[i].diario,self.gridOptions.data[i].tipo),
              'dev':self.gridOptions.data[i].devuelto.toString(),
              'pag':self.gridOptions.data[i].pagar.toString(),
              'pu':self.gridOptions.data[i].precio_venta.toString(),
              'sub':sub_total.toString(),
            };
            self.items.push(rows);
          }
      }
    }

    //metodo de impresion directa de html
    self.printDiv = function(divName) {
      var printContents = document.getElementById(divName).innerHTML;
      var originalContents = document.body.innerHTML;
      document.body.innerHTML = printContents;
      window.print();
      document.body.innerHTML = originalContents;
    }

    }
}())

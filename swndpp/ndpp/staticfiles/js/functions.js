function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function recargar(div, destino){
   $(div).load(destino);
}


//*****************************************************************

function save_guide(factura, guia){
  console.log('guardando guia');
  var parametros = {
    "voucher" : parseInt(factura),
    "guide" : parseInt(guia)
  };
  $.ajax({
    data:  parametros, //datos que se envian a traves de ajax
    url:   '/api/save-guide/voucher', //archivo que recibe la peticion
    type:  'post', //método de envio
  });
  location.reload(true);
}


function delete_guide(factura, guia){
  var parametros = {
    "voucher" : parseInt(factura),
    "guide" : parseInt(guia)
  };
  $.ajax({
    data:  parametros, //datos que se envian a traves de ajax
    url:   '/api/delete-guide/voucher', //archivo que recibe la peticion
    type:  'post', //método de envio
  });
  location.reload(true);
}

// funcion para imprimir una guia
function imprimir_liquidacion(name){
  console.log('entrando a imprimir');
  $("#lista-facturas").table2excel({
      filename: name
  });
}

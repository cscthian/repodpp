$(function(){

  var toggleMenu = $('#togle-menu');
  var nav = $('#nav-menu');

  toggleMenu.on('click',function(){
    nav.toggleClass('mostrar-menu');
  });

  nav.on('click',function(){
    console.log('*****');
    nav.removeClass('mostrar-menu').addClass('nav-menu');
  });
});

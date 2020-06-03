(function(){
    "use strict";
    angular.module("common.services")
        .filter("DateRangeFilter", [DateRangeFilter]);

        function DateRangeFilter(){
          return function(date, fecha1, fecha2){
            for (var d in date) {
              if (d.created<=fecha1 && d.created>=fecha2) {
                return d;
                console.log(d);
              }
            }

          }
        };
}());

(function(){
    "use strict";

    angular.module("common.services")
        .factory("guideServices",guideServices);

    function guideServices($http){
        return $http.get("/api/magazine");

    }
}());

webStub.ready(function(stub, global, config){

    var Application = stub.Class('Application', {
        global: global
        , stub: stub
        , core: webStub

        , init: function(name){
            console.log('new Application')
            this.name = name;
        }
    });
});
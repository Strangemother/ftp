/*
Write a basic component to work upon until all precendences are set.
 */
;(function(global){
    var stub = {};
    var globalName = 'webStub';
    var config = {};
    var configured = false;
    var adds = [];
    // methods to be called on run.
    var readys = []

    var main = function(){
        writeStub(stub);
    };

    var writeStub = function(_stub){
        _stub.resolve = resolve;
        _stub.configure = configure;
        _stub.run = run
        _stub.ready = readyApp
        _stub.events = new MicroEvents();
        _stub.templates = rivets;

        _stub.add = function(path, v) {
            adds.push([path, v]);
            if(configured){
                implementAdds(adds)
            }
        };

        global[globalName] = _stub
    };

    var implementAdds = function(adds) {
        // implement each class.

        for (var i = 0; i < adds.length; i++) {
            var add = adds[i];

            /*
             we mark undefined in place of element
             for later cleanup - this is cleaner than slicing the array
             */
            adds[i] = undefined
            add && makeObj(stub, add[0], add[1])
        };
    };

    var implementReadys = function(stub, global, config) {
        /*
         run each ready function implementing the
         chain callback on run method.
         */

        /*
         The exoScope is provided to the incoming function,
         any changes to the exoScope can be maintained externally
         before and after the functional scope provided.

         allowing `this` reference for scoped alterations.
         */
        var exoScope = {};

        for (var i = 0; i < readys.length; i++) {
            var f= readys[i];
            /*
             we mark undefined in place of element
             for later cleanup - this is cleaner than slicing the array
             */
            readys[i] = undefined;
            f && f.call(exoScope, stub, global, config);
        };
        reactTo(exoScope)
    }

    var reactTo = function(exoScope) {
        /*
        an exoScope was passed to a ready method
        upon call. The exoScope may contain additional
        information about the called function to be
        manipulated later.
         */
        console.log('implemented ready scope')
    }

    var configure = function(obj) {
        if(obj!== undefined) {
            config = obj;
            if(config.autoRun !== false) {
                return run()
            }
            return stub;
        }

        return obj
    };

    var run = function(cb){

        makeObj(global, config.scope, stub)
        configured = true;
        implementAdds(adds);
        implementReadys(stub, global, config)

        rivets.configure(config.templates)

        cb && cb()
        return stub;
    };

    var readyApp = function(f) {
        /*
        a function to be called when the run is performed.
         */
        console.log('pushing ready callback')

        if(readys.indexOf(f) > -1) {
            throw new Error('ready callback already applied')
            return false;
        }

        readys.push(f);
        if(configured) {
            implementReadys(stub, global, config)
        }
    };

    var resolve = function(str, errord){
        var obj = global;
        if( arguments.length === 2) {
            if( it(errord).is('object') ) {
                obj = errord
                errord = true;
            }
        } else if(arguments.length === 3) {
            obj = arguments[0]
            s = arguments[1]
            errord = arguments[2]
        }

        // Error should be default true for this
        errord = errord || (this.silent) ? false: true;
        // splitString and return object
        var keys = str.split('.');
        var key;

        for (var i = 0; i < keys.length; i++) {
            key = keys[i];
            if( key && obj && key in obj
                || ( obj.hasOwnProperty
                    && obj.hasOwnProperty(key) )
            ) {
                obj = obj[key]
            } else {
                obj=undefined
                if(errord === true) {
                    // Could not resolve key in window
                    var preKey = i-1 > 0 ? obj[i-1]: 'window';
                    console.error('Could not resolve', key, 'in', preKey)
                }
                return obj
            }
        };
        return obj;
    }

    var makeObj = function(schema, path, value) {
        var pList = path.split('.');
        var len = pList.length;
        for(var i = 0; i < len-1; i++) {
            var elem = pList[i];
            if( !schema[elem] ) schema[elem] = {}
            schema = schema[elem];
        }

        schema[pList[len-1]] = value;
    };

    main();
}).apply({}, [window])
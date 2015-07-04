/*
Write a basic component to work upon until all precendences are set.
 */
;(function(global){
    var stub = {};
    var globalName = 'webStub';
    var config = {};
    var adds = [];

    var main = function(){
        writeStub(stub);
    };

    var writeStub = function(_stub){
        _stub.resolve = resolve;
        _stub.configure = configure;
        _stub.run = run

        _stub.add = function(path, v) {
            adds.push([path, v]);
        };

        global[globalName] = _stub
    };

    var implementAdds = function(adds) {
        // implement each class.
        var scope = resolve(config.scope)
        for (var i = 0; i < adds.length; i++) {
            var add = adds[i];
            m = makeObj(scope, add[0], add[1])
        };
    };

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
        implementAdds(adds);
        cb && cb()
        return stub;
    }

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
}).apply({}, [window]);/*
convert internal defined classes to the adapter
 */
;(function(global){

    var main = function(){
        wrappers(this)
    };

    var wrappers = function(stub) {
        webStub.Class = writeClass
    }

    var writeClass = function(name, def) {
        // Returns the def
        var parent = getParent(def);
        // get mixins and extentions
        var mixins = getMixins(def);
        var cleanDef = clean(name, def);
        // merge the two extenders
        var inherits
        var klass;
        if(parent !== undefined) {
            inherits = [parent].concat(mixins);
        } else {
            inherits = mixins;
        }
        if(inherits.length == 0) {
            klass = jsface.Class(cleanDef)
        } else {
            klass = jsface.Class(inherits, cleanDef)
        }

        webStub.add(name, klass)
        return klass;
    };

    var getParent = function(def) {
        var p = def['Extends'];
        delete def['Extends'];
        return p;
    }

    var getMixins = function(def) {
        var p = def['Implements'];
        delete def['Implements'];
        if( p == undefined) {
            return []
        }
        return p;
    }

    var globalConstruct = function(){
        // Basic constructor for all
        // inbound classes without the 'constructor'
        // definition in the view.
        return function constructor() {

            if(this === window) {
                throw new Error('class need "new" instansiation')
            }

            if(this.init !== undefined){
                return this.init.apply(this, arguments);
            }
        }
    };

    var clean = function(name, def) {
        if( !def['constructor']
            || def.constructor == Object ){
            def['constructor'] = globalConstruct()
        };

        var ns = name.split('.')
        if( !def['type'] ) {
            // write a type
            def.type = ns[ns.length-1]
        };

        return def;
    }

    main();

}).apply(webStub, [window]);
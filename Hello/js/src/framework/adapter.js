/*
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
        console.log('adding class', name)
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
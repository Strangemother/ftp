webStub.ready(function(stub, global, config){

    var Template = stub.Class('ui.Template', {
        /* will automatically attach to data-template=Name */
        init: function(name, model) {
            this.name = name;
            this.model = model || {
                _template_name: this.name
            };
        }

        , bind: function(view, model){
            this.unbind()
            if(view===undefined) view=this.view;
            if(model===undefined) model=this.model;

            this.view = stub.templates.bind(view, model)
            return this.view
        }

        , unbind: function(){
            if(this.view) {
                this.view.unbind()
            };
        }

        , on: function(){
            if(!this.delegator) {
                this.delegator = new Gator(this.view)
            }
            return this.delegator.on.apply(this.delegator, arguments);
        }

        , off: function(){
            if(this.delegator) {
                this.delegator.off.apply(this.delegator, arguments)
            }
        }

        , destroy: function() {
            if(this.delegator){
                this.delegator.off()
            }
            this.unbind()
        }

        , copy: function(){
            var element = this.element();
            return $(element).html()
        }

        , element: function(name){
            if(name !== undefined) {
                var el = $(name);
                // try selector
                if( el.length == 0 ) {
                    el = $('*[data-template="' + name + '"]')
                };

                if( el.length == 0 ) {
                    return false;
                };
                // try edit selector
                this._element = el;
                return this;
            };

            return this._element;
        }

        , render: function(model, toSelector) {
            var $element = $( this.element(name).copy() );
            model = model || this.model || {};
            toSelector = toSelector || this.target;

            $element.appendTo(toSelector);


            var view = this.bind($element, model);
            return view;
        }

        , load: function(name, target) {
            /*
             load a HTML template from a server path. The Template is
             predefined to look for 'pages' subdirectory relative from it's
             load directory.

             The result will be pushed into `this.target` or `this.element()`
             respectively.

             The `element` defined can be a selector at Template instantiation or
             a special name defined selectable by the data-template selector.
             */

            // returns path: /pages/name.html
            name = name || this.name;
            var pageLoaded = function(){
                console.log('pageLoaded')
            }

            target = target || this.target;
            if(target===undefined) {
                target = this.element(name).copy();
            };

            $(target).load('pages/' + name + '.html', pageLoaded)
            // $(target)[0].innerHTML='<object type="text/html" id="template_' + name +'" data="html/'+name+'.html" ></object>';
        }
    });

    var main = function(){
        stub.app = new stub.Application('interface');
        var t = new Template('interface')

    };

    stub.ready(main)
});
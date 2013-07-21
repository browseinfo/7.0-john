openerp.google_docs_addlink = function(instance, m) {
var _t = instance.web._t,
    QWeb = instance.web.qweb;

    instance.web.Sidebar.include({
        redraw: function() {
            var self = this;
            console.log(":::::::>>>>>>>>>>",self);
            this._super.apply(this, arguments);
            self.$el.find('.oe_sidebar_add_attachment').after(QWeb.render('AddGoogleDocumentItem1', {widget: self}))
            self.$el.find('.oe_sidebar_add_google_button').on('click', function (e) {
                self.on_change_button();
            });
        },
       

       on_change_button: function() {
            var self = this;
            var view = self.getParent();
            var from=this.$el.find('#msg').val();
            var ids = ( view.fields_view.type != "form" )? view.groups.get_selection().ids : [ view.datarecord.id ];
           
           var ids = ( view.fields_view.type != "form" )? view.groups.get_selection().ids : [ view.datarecord.id ];
            if( !_.isEmpty(ids) ){
                view.sidebar_eval_context().done(function (context) {
                    var ds = new instance.web.DataSet(this, 'ir.attachment', context);
                    context = {'url':from}
                    ds.call('google_doc_url', [view.dataset.model, ids, context]).done(function(r) {
                    
                        if (r == 'False') {
                            var params = {
                                error: response,
                                message: _t("The user google credentials are not set yet. Contact your administrator for help.")
                            }
                            $(openerp.web.qweb.render("DialogWarning", params)).dialog({
                                title: _t("User Google credentials are not yet set."),
                                modal: true,
                            });
                        }
                    }).done(function(r){
                        view.reload();
                    });
                });
            
 

        }
         },


        on_google_doc: function() {
            var self = this;
            var view = self.getParent();
           
            
       
        }
        
         });
};

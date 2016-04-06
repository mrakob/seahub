define([
    'jquery',
    'underscore',
    'backbone',
    'common',
    'moment',
    'sysadmin-app/views/device',
    'sysadmin-app/collection/devices'
], function($, _, Backbone, Common, Moment, Device, DevicesCollection) {
    'use strict';

    var DevicesView = Backbone.View.extend({

        id: 'admin-devices',

        template: _.template($("#admin-devices-tmpl").html()),

        initialize: function() {
            this.devicesPageableCollection = new DevicesCollection();
            this.listenTo(this.devicesPageableCollection, 'add', this.addOne);
            this.listenTo(this.devicesPageableCollection, 'reset', this.reset);
            this.render();
        },

        events: {
            'click #paginator .paginator-next': 'getNextPage',
            'click #paginator .paginator-previous': 'getPreviousPage'
        },

        getNextPage: function() {
            if (this.hasNextPage) {
                this.devicesPageableCollection.getNextPage({'reset': true});
            }
            return false;
        },

        getPreviousPage: function() {
            if (this.devicesPageableCollection.state.currentPage > 0) {
                this.devicesPageableCollection.getPreviousPage({'reset': true});
            }
            return false;
        },

        addOne: function(device) {
            var view = new Device({model: device});
            this.$tableBody.append(view.render().el);
        },

        render: function() {
            this.$el.html(this.template({'cur_tab': 'devices'}));
            this.$table = this.$('table');
            this.$tableBody = $('tbody', this.$table);
            this.$pagePrevious = this.$('.paginator-previous');
            this.$pageNext = this.$('.paginator-next');
            this.$loadingTip = this.$('.loading-tip');
            this.$emptyTip = this.$('.empty-tips');
            return this;
        },

        hide: function() {
            this.$el.detach();
        },

        show: function() {
            $("#right-panel").html(this.$el);
            this.showAdminDevices();
        },

        showAdminDevices: function() {
            this.$table.hide();
            this.$loadingTip.show();

            var _this = this;
            this.devicesPageableCollection.fetch({
                cache: false, // for IE
                reset: true,
                success: function (collection, response, opts) {
                },
                error: function (collection, response, opts) {
                    var err_msg;
                    if (response.responseText) {
                        if (response['status'] == 401 || response['status'] == 403) {
                            err_msg = gettext("Permission error");
                        } else {
                            err_msg = $.parseJSON(response.responseText).error_msg;
                        }
                    } else {
                        err_msg = gettext("Failed. Please check the network.");
                    }
                    Common.feedback(err_msg, 'error');
                }
            });
        },

        reset: function() {
            var length = this.devicesPageableCollection.length;
            var current_page = this.devicesPageableCollection.state.currentPage;

            this.$loadingTip.hide();

            if (length > 0) {
                this.$emptyTip.hide();
                this.$tableBody.empty();
                this.devicesPageableCollection.each(this.addOne, this);
                this.$table.show();

                if (length == 100) {
                    this.hasNextPage = true;
                    this.$pageNext.show();
                } else {
                    this.hasNextPage = false;
                }

            } else {
                if (current_page == 0) {
                    this.$table.hide();
                    this.$emptyTip.show();
                }
            }

            if (current_page == 0) {
                this.$pagePrevious.hide();
            } else {
                this.$pagePrevious.show();
            }
        }

    });

    return DevicesView;
});

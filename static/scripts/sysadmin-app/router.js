/*global define*/
define([
    'jquery',
    'backbone',
    'common',
    'sysadmin-app/views/side-nav',
    'sysadmin-app/views/dashboard',
    'sysadmin-app/views/devices',
    'sysadmin-app/views/device-errors'
], function($, Backbone, Common, SideNavView,
    DashboardView, DevicesView, DeviceErrorsView) {
    "use strict";

    var Router = Backbone.Router.extend({
        routes: {
            '': 'showDashboard',
            'dashboard/': 'showDashboard',
            'admin-all-devices/': 'showDevices',
            'admin-device-errors/': 'showDeviceErrors',
            // Default
            '*actions': 'showDashboard'
        },

        initialize: function() {
            Common.prepareApiCsrf();
            Common.initLocale();
            Common.initAccountPopup();

            this.sideNavView = new SideNavView();
            app.ui = {
                sideNavView: this.sideNavView
            };

            this.dashboardView = new DashboardView();
            this.deviceErrorsView = new DeviceErrorsView();
            this.devicesView = new DevicesView();

            this.currentView = this.dashboardView;

            $('#info-bar .close').click(Common.closeTopNoticeBar);
        },

        switchCurrentView: function(newView) {
            if (this.currentView != newView) {
                this.currentView.hide();
                this.currentView = newView;
            }
        },

        showDashboard: function() {
            this.switchCurrentView(this.dashboardView);
            this.sideNavView.setCurTab('dashboard');
            this.dashboardView.show();
        },

        showDevices: function() {
            this.switchCurrentView(this.devicesView);
            this.sideNavView.setCurTab('devices');
            this.devicesView.show();
        },

        showDeviceErrors: function() {
            this.switchCurrentView(this.deviceErrorsView);
            this.sideNavView.setCurTab('devices');
            this.deviceErrorsView.show();
        }

    });

    return Router;
});

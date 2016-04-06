define([
    'underscore',
    'backbone',
    'backbone.paginator',
    'common',
    'sysadmin-app/models/device'
], function(_, Backbone, BackbonePaginator, Common, Device) {
    'use strict';

    var DevicesCollection = Backbone.PageableCollection.extend({
        model: Device,
        state: {
            currentPage: 0,
            pageSize: 100,
        },
        url: function () {
            return Common.getUrl({name: 'admin-devices'});
        }
    });

    return DevicesCollection;
});

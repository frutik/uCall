/**
 * @class uCall.widgets.MainTopToolbar
 * @extends Ext.toolbar.Toolbar
 *
 * Shows main top toolbar.
 */

Ext.define('uCall.widgets.MainTopToolbar', {
    requires: [
        'uCall.widgets.UserStatusMenuButton',
        'uCall.widgets.UserServiceMenuButton',
        'uCall.widgets.ChannelStatusIndicator'
    ],
    extend: 'Ext.toolbar.Toolbar',
    alias: 'widget.MainTopToolbar',
    
    config: {
        id: 'MainTopToolbar',
        items: [
            {xtype: 'ChannelStatusIndicator'},
            configApp.name,
            '->',
            {xtype: 'UserStatusMenuButton'},
            '-',
            {xtype: 'UserServiceMenuButton'}
        ]
    },
    
    constructor: function(){
        Ext.applyIf(this, this.config);
        this.callParent(arguments);
    }
});
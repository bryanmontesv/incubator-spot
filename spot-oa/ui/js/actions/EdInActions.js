// Licensed to the Apache Software Foundation (ASF) under one or more contributor license agreements; and to You under the Apache License, Version 2.0.

var SpotDispatcher = require('../dispatchers/SpotDispatcher');
var SpotActions = require('./SpotActions');
var SpotConstants = require('../constants/SpotConstants');
var SpotUtils = require('../utils/SpotUtils');

var EdInActions = {
  setFilter: function (filter)
  {
    SpotUtils.setUrlParam('filter', filter);

    SpotDispatcher.dispatch({
      actionType: SpotConstants.UPDATE_FILTER,
      filter: filter
    });
  },
  reloadSuspicious: function () {
    SpotActions.toggleMode(SpotConstants.DETAILS_PANEL, SpotConstants.DETAILS_MODE);
    SpotDispatcher.dispatch({
      actionType: SpotConstants.RELOAD_SUSPICIOUS
    });
  },
  reloadDetails: function () {
    SpotDispatcher.dispatch({
      actionType: SpotConstants.RELOAD_DETAILS
    });
  },
  reloadVisualDetails: function () {
    SpotDispatcher.dispatch({
      actionType: SpotConstants.RELOAD_DETAILS_VISUAL
    });
  },
  highlightThreat: function (id)
  {
    SpotDispatcher.dispatch({
      actionType: SpotConstants.HIGHLIGHT_THREAT,
      threat: id
    });
  },
  unhighlightThreat: function ()
  {
    SpotDispatcher.dispatch({
      actionType: SpotConstants.UNHIGHLIGHT_THREAT
    });
  },
  selectThreat: function (threat)
  {
    SpotDispatcher.dispatch({
      actionType: SpotConstants.SELECT_THREAT,
      threat: threat
    });
  },
  selectIp: function (ip)
  {
    SpotDispatcher.dispatch({
      actionType: SpotConstants.SELECT_IP,
      ip: ip
    });
  },
  saveScoring: function(scoredEmelents) {                   //Save all the scored IPS, hosts & ports and the page reload all the components again
    SpotDispatcher.dispatch({
      actionType: SpotConstants.SAVE_SCORED_ELEMENTS,
      scoredElems: scoredEmelents
    });
  },
  resetScoring: function(date) {                           //Reset all scored IPS, hosts & ports and the page reload all the components again
    SpotDispatcher.dispatch({
      actionType: SpotConstants.RESET_SCORED_ELEMENTS,
      date: date
    });
  },
  setClassWidth: function(validate) {                      //Change a class from scoring to split the space in case of available scoring widgets, if not scoring will take all the space
    SpotDispatcher.dispatch({
      actionType: SpotConstants.CHANGE_CSS_CLS,
      validate: validate
    });
  },
  getWidgets: function(wtype, pipeline) {                  //When the page is loaded it send an action to get all avaliable plugins
    SpotDispatcher.dispatch({
      actionType: SpotConstants.GET_WIDGETS,
      wtype: wtype,
      pipeline: pipeline
    });
  },
  sendWidgetMethodData: function() {                      //Send data from loaded widgets (they need to have another store to execute an action)
    SpotDispatcher.dispatch({
      actionType: SpotConstants.SEND_DATA_FROM_WIDGET
    });
  },
  changeMenu: function() {                                //Check if the Menu has changed when a widget from plugins is loaded
    SpotDispatcher.dispatch({
      actionType: SpotConstants.RELOAD_MENU
    });
  },
  enableDisablePlugin: function(name, status) {                       //Enable/disable a plugin, send an action to restart all services
    SpotDispatcher.dispatch({
      actionType: SpotConstants.RESTART_SERVICE,
      name: name,
      status: status
    });
  }
};

module.exports = EdInActions;

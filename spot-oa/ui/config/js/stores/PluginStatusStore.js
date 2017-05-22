// Licensed to the Apache Software Foundation (ASF) under one or more contributor license agreements; and to You under the Apache License, Version 2.0.

const SpotDispatcher = require('../../../js/dispatchers/SpotDispatcher');
const SpotConstants = require('../../../js/constants/SpotConstants');

const ObservableWithHeadersGraphQLStore = require('../../../js/stores/ObservableWithHeadersGraphQLStore');

const NAME = 'name';
const STATUS = 'status';

class PluginStatusStore extends ObservableWithHeadersGraphQLStore {
    constructor() {
        super();
        this.query =  `
            query ($name: String!, $status: Boolean){
              config {
                pluginsStatus(name: $name, status: $status) {
                  status
                  name
                }
              }
            }
          `;
    }

    getQuery() {
        return this.query;
    }

    enableDisablePlugin(name, status) {
      this.setVariable(NAME, name);
      this.setVariable(STATUS, status);
    }

    unboxData(data) {
        return data.config.pluginsStatus;
    }
}

const ps = new PluginStatusStore();

SpotDispatcher.register(function (action) {
    switch (action.actionType) {
        case SpotConstants.RESTART_SERVICE:
            ps.enableDisablePlugin(action.name, action.status);
            ps.sendQuery();
            break;
    }
});

module.exports = ps;

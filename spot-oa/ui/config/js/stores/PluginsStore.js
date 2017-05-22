// Licensed to the Apache Software Foundation (ASF) under one or more contributor license agreements; and to You under the Apache License, Version 2.0.

const SpotDispatcher = require('../../../js/dispatchers/SpotDispatcher');
const SpotConstants = require('../../../js/constants/SpotConstants');

const ObservableWithHeadersGraphQLStore = require('../../../js/stores/ObservableWithHeadersGraphQLStore');

const WTYPE = 'wtype';
const PIPELINE = 'pipeline';
const NAME = 'name';
const STATUS = 'status';

class PluginsStore extends ObservableWithHeadersGraphQLStore {
    constructor() {
        super();
        this.query = `
            query ($wtype: String!, $pipeline: String){
              config {
                pluginsWidgets(wtype: $wtype, pipeline: $pipeline) {
                  complete_schema
                }
              }
            }
          `;
    }

    getQuery() {
        return this.query;
    }

    getWidgets(wtype, pipeline) {
      this.setVariable(WTYPE, wtype);
      this.setVariable(PIPELINE, pipeline);
    }

    unboxData(data) {
        return data.config.pluginsWidgets;
    }
}

const ps = new PluginsStore();

SpotDispatcher.register(function (action) {
    switch (action.actionType) {
        case SpotConstants.GET_WIDGETS:
            ps.getWidgets(action.wtype, action.pipeline);
            ps.sendQuery();
            break;
    }
});

module.exports = ps;

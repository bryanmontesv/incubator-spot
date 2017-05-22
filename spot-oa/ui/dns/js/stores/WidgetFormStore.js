// Licensed to the Apache Software Foundation (ASF) under one or more contributor license agreements; and to You under the Apache License, Version 2.0.

const SpotDispatcher = require('../../../js/dispatchers/SpotDispatcher');
const SpotConstants = require('../../../js/constants/SpotConstants');

const ObservableWithHeadersGraphQLStore = require('../../../js/stores/ObservableWithHeadersGraphQLStore');

const WTYPE = 'wtype';
const PIPELINE = 'pipeline';
const WILLBLOCK = 'ip';

class WidgetDataStore extends ObservableWithHeadersGraphQLStore {
    constructor() {
        super();
        this.endPoint = '';
        this.query = `
            query ($wtype: String, $pipeline: String) {
              config {
                pluginsWidgets(wtype: $wtype, pipeline: $pipeline) {
                  complete_json
                }
              }
            }
            `;
        this.ip = '';
        this.formData = {};
        this.lastFormData = {};
    }

    getQuery() {
        return this.query;
    }

    getWidgets(wtype, pipeline) {
      Object.keys(this.lastFormData).forEach((elem) => {
        this.unsetVariable(elem);
      });
      this.unsetVariable(WILLBLOCK);

      this.setVariable(WTYPE, wtype);
      this.setVariable(PIPELINE, pipeline);
    }

    unboxData(data) {
        return data.config ? data.config.pluginsWidgets : data;
    }
}

const ws = new WidgetDataStore();

SpotDispatcher.register(function (action) {
    switch (action.actionType) {
        case SpotConstants.GET_WIDGETS:
            ws.getWidgets(action.wtype, action.pipeline);
            ws.sendQuery();
            break;
    }
});

module.exports = ws;

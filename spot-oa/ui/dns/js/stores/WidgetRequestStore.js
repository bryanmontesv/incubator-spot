// Licensed to the Apache Software Foundation (ASF) under one or more contributor license agreements; and to You under the Apache License, Version 2.0.

const SpotDispatcher = require('../../../js/dispatchers/SpotDispatcher');
const SpotConstants = require('../../../js/constants/SpotConstants');

const ObservableWithHeadersGraphQLStore = require('../../../js/stores/ObservableWithHeadersGraphQLStore');

const WILLBLOCK = 'ip';

class WidgetRequestStore extends ObservableWithHeadersGraphQLStore {
    constructor() {
        super();
        this.endPoint = '';
        this.query = '';
        this.ip = '';
        this.formData = {};
        this.lastFormData = {};
    }

    getQuery() {
        return this.query;
    }

    sendDataFromWidget() {
      Object.keys(this.lastFormData).forEach((elem) => {
        this.unsetVariable(elem);
      });
      this.unsetVariable(WILLBLOCK);

      Object.keys(this.formData).forEach((elem) => {
        this.setVariable(elem, this.formData[elem]);
      });
      this.setVariable(WILLBLOCK, this.ip);
      this.lastFormData = this.formData;
    }

    unboxData(data) {
        return data;
    }

}

const wrs = new WidgetRequestStore();

SpotDispatcher.register(function (action) {
    switch (action.actionType) {
        case SpotConstants.SEND_DATA_FROM_WIDGET:
            wrs.sendDataFromWidget();
            wrs.sendQuery();
            break;
    }
});

module.exports = wrs;

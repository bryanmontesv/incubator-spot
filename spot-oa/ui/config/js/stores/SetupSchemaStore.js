// Licensed to the Apache Software Foundation (ASF) under one or more contributor license agreements; and to You under the Apache License, Version 2.0.

const SpotDispatcher = require('../../../js/dispatchers/SpotDispatcher');
const SpotConstants = require('../../../js/constants/SpotConstants');

const ObservableWithHeadersGraphQLStore = require('../../../js/stores/ObservableWithHeadersGraphQLStore');

class SetupSchemaStore extends ObservableWithHeadersGraphQLStore {
    constructor() {
        super();
        this.endPoint = '';
        this.query = '';
        this.formData = {};
        this.lastFormData = {};
        this.name = '';
    }

    getQuery() {
        return this.query;
    }

    sendDataFromWidget() {
      Object.keys(this.lastFormData).forEach((elem) => {
        this.unsetVariable(elem);
      });

      Object.keys(this.formData).forEach((elem) => {
        this.setVariable(elem, this.formData[elem]);
      });
      this.lastFormData = this.formData;
    }

    unboxData(data) {
        return data;
    }

}

const sss = new SetupSchemaStore();

SpotDispatcher.register(function (action) {
    switch (action.actionType) {
        case SpotConstants.SEND_DATA_FROM_WIDGET:
            sss.sendDataFromWidget();
            sss.sendQuery();
            break;
    }
});

module.exports = sss;

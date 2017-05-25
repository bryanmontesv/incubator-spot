// Licensed to the Apache Software Foundation (ASF) under one or more contributor license agreements; and to You under the Apache License, Version 2.0.

var React = require('react');

const EdInActions = require('../../../js/actions/EdInActions');
const PluginsStore = require('../stores/PluginsStore');
const PluginStatusStore = require('../stores/PluginStatusStore');
const SetupSchemaStore = require('../stores/SetupSchemaStore');
const SpotConstants = require('../../../js/constants/SpotConstants');
const SpotUtils = require('../../../js/utils/SpotUtils');
const SwitchToggleButton = require('../../../js/components/SwitchToggleButton.react');
const SpotModal = require('../../../js/components/SpotModal.react');

import Form from "react-jsonschema-form";

var PluginController = React.createClass({
  emptySetMessage: 'There aren\'t plugins installed.' ,
  getInitialState: function () {
    return {
      plugins: []
    };
  },
  componentDidMount: function() {
    this.setState({ isChecked: this.props.isChecked });
    PluginsStore.addChangeDataListener(this._onChange);
    SetupSchemaStore.addChangeDataListener(this._onResponseChange);
    PluginStatusStore.addChangeDataListener(this._onChangePlugins);
  },
  componentWillUnmount: function () {
    PluginsStore.removeChangeDataListener(this._onChange);
    SetupSchemaStore.removeChangeDataListener(this._onResponseChange);
    PluginStatusStore.removeChangeDataListener(this._onChangePlugins);
  },
  render: function() {
    let plugin_body, plugin_headers, content, gridBody = [],
        {state = [], requests = [], pluginsStatus = []} = {
                                                            state: this.state.plugins,
                                                            requests:this.state.response,
                                                            pluginsStatus: this.state.pluginsStatus
                                                          };
    let gridHeaders = ['Plugin Name', 'Version', 'Description', 'Enable/Disable', 'View/Edit'];
    const log = (methodSchema, endpoint, type ) => this.callMethod.bind(methodSchema, endpoint, type);

    //check if request data did respond good or bad when the user submitted data
    if(requests.data && JSON.stringify(requests.data).indexOf('"status":true') !== -1) {
      swal('Success!', 'The service ' + Object.keys(requests.data)[0] + ' respond with success', 'success');
      EdInActions.getWidgets('scoring,menu', '');
    } else if(requests.data && JSON.stringify(requests.data).indexOf('"status":false') !== -1){
      swal('Error!', 'The service ' + Object.keys(requests.data)[0] + ' respond with an error, please verify', 'error');
    }

    //this message will show when the user enabled or disabled a plugin
    pluginsStatus.forEach((elem, i) => {
      let composeMsg = elem.status == true ? 'enabled correctly' : 'disabled, some features can disappear from UI'
      let title = elem.status ? 'Success!' : 'Warning!',
          message = 'Plugin ' + elem.name + ' has been ' + composeMsg,
          action = elem.status ? 'success' : 'warning';
      swal(title, message, action);
    });

    //check if state has data
    if (state.error) {
      content = (
        <div className="text-center text-danger">
          {state.error}
        </div>
      );
    } else if (state.loading) {
      content = (
        <div className="spot-loader">
          Loading <span className="spinner"></span>
        </div>
      );
    } else if (!state.data || state.data.length === 0) {
      content = (
        <div className="text-center">
          {this.emptySetMessage || ''}
        </div>
      );
    } else {

      plugin_headers = gridHeaders.map((elem, i) =>
        <th key={'th_' + elem} className={'text-center ' + elem}>{elem}</th>
      );

      //if state has data then it will check for the data that will be placed on plugins table
      state.data.forEach((elem, index) => {
        let data = JSON.parse(elem.complete_schema.replace(/\'/g, '"'));
        gridBody.push({plugin_name: data.metadata['plugin_name'], version: data.metadata['plugin_version'], description: data.metadata['plugin_description'], status: false, conf: 'plugin.json' });
      });

      plugin_body = gridBody.map((elem, index) => {
        let cells, data = state ? JSON.parse(state.data[index].complete_schema.replace(/\'/g, '"')) : '';

        cells = Object.keys(elem).map((e, i) => {
          let typeElement;
          switch (e) {
            case 'status':
              typeElement = (
                <SwitchToggleButton isChecked={elem[e]} name={elem['plugin_name']} onChange={this.onEnableDisable}/>
              )
            break;
            case 'conf':
              if (typeof data.setup_schema !== "undefined" && Object.keys(data.setup_schema).length > 0) {
                typeElement = (
                  <SpotModal title={elem['plugin_name']}
                    body={
                      <Form schema={data.setup_schema.schema} uiSchema={data.setup_schema.uiSchema || {}} formData={data.setup_schema.formData || {}} onSubmit={log('submitted', data.metadata || {}, data.setup_schema.method || '')} onError={log('errors'), false} />
                    }/>
                )
              }
            break;
            default:
              typeElement = elem[e];
            break;
          }

          return (
            <td key={'td_' + i} className={'text-center ' + e}>
              {typeElement}
            </td>
          )
        })
        return (
          <tr key={'tr_' + index}>{cells}</tr>
        )
      });
      content = (
        <table className="table table-intel table-intel-striped table-hover" style={{fontSize: 'small'}}>
          <thead>
            <tr>
              {plugin_headers}
            </tr>
          </thead>
          <tbody>
            {plugin_body}
          </tbody>
        </table>
      );
    }
    return(
      <div className="spot-grid-panel col-md-12">
        {content}
      </div>
    );
  },
  _onChange: function() {
    let plugins = PluginsStore.getData();
    this.replaceState({plugins});   //we need to replace data because it need to empty the other 2 onChange methods
  },
  _onResponseChange: function() {
    let response = SetupSchemaStore.getData();
    this.setState({response});      //when this response is executed, it will send a message saying what was the plugins return
  },
  _onChangePlugins: function() {
    let pluginsStatus = PluginStatusStore.getData();
    this.setState({pluginsStatus: pluginsStatus.data});   //this response will respond with a true or false in case a plugin enabled or disabled
  },
  callMethod: function(metadata, query, obj) {
    SetupSchemaStore.endPoint = metadata.endpoint;
    SetupSchemaStore.query = query;
    SetupSchemaStore.formData = obj.formData;
    SetupSchemaStore.name = metadata.plugin_name;

    EdInActions.sendWidgetMethodData();
  },
  onEnableDisable: function(name, status) {
    EdInActions.enableDisablePlugin(name, status);
  }
});

module.exports = PluginController;

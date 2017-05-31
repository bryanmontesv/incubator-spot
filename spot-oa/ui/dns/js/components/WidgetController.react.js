// Licensed to the Apache Software Foundation (ASF) under one or more contributor license agreements; and to You under the Apache License, Version 2.0.

var React = require('react');


const EdInActions = require('../../../js/actions/EdInActions');
const SpotConstants = require('../../../js/constants/SpotConstants');
const SpotUtils = require('../../../js/utils/SpotUtils');
const Menu = require('../../../js/menu/menu');
const WidgetFormStore = require('../stores/WidgetFormStore');
const WidgetRequestStore = require('../stores/WidgetRequestStore');


import Form from "react-jsonschema-form";

var WidgetController = React.createClass({
  emptySetMessage: 'There aren\'t plugins installed.' ,
  getInitialState: function () {
    return {
      schema: {}
    };
  },
  componentDidMount: function() {
    WidgetFormStore.addChangeDataListener(this._onChange);
    WidgetRequestStore.addChangeDataListener(this._onChange);
  },
  componentWillUnmount: function () {
    WidgetFormStore.removeChangeDataListener(this._onChange);
    WidgetRequestStore.removeChangeDataListener(this._onChange);
  },
  render: function() {
    let plugins, content, schema = this.state.data || []
                        , requests = this.state.requests || [];
    let validateWidgetsToShow = false;

    const log = (methodSchema, endpoint, type) => this.callMethod.bind(methodSchema, endpoint, type);
    /*this is an accordion. It will check if there is an schema to loop, if it does,
    it will check the types of widgets, and look which action correspond to each one*/

    //first, validate if request or schema has data, if it does then apply some functions
    if(requests.data && JSON.stringify(requests.data).indexOf('"status":true') !== -1) {
      let msg = "The action you deployed was made successfully on";
      let pluginObj = requests.data[Object.keys(requests.data)[0]];
      let propsPluginResponse = pluginObj[Object.keys(pluginObj)[0]][0].msg;
      if(propsPluginResponse) {
        msg = propsPluginResponse || "Error"
      }

      swal({
        title: 'Success',
        text:  msg + ': ' + WidgetRequestStore.ip,
        type: 'success',
        showCancelButton: false,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Continue'
      }).then(() => {

      });
    } else if(requests.data && JSON.stringify(requests.data).indexOf('"status":false') !== -1){
      let msg = "There were an error trying to deploy an action on";
      let pluginObj = requests.data[Object.keys(requests.data)[0]];
      let propsPluginResponse = pluginObj[Object.keys(pluginObj)[0]][0].msg;
      if(propsPluginResponse) {
        msg = propsPluginResponse || "Error"
      }
      swal('Error!', msg + ': ' + WidgetRequestStore.ip, 'error');
    }
    if(schema.data) {
      plugins = schema.data.map((data, i) => {
        data = JSON.parse(data.complete_json.replace(/\'/g, '"'))
        if(data.metadata.status === 1) {
          switch (data.metadata.type) {
            case 'menu':
              this.makeMenu(data);
            break;
            default:
              validateWidgetsToShow = data.metadata.type === 'scoring' && this.props.show === 'all'
              let ids = new Date().getTime();
              return (
                <div className="panel panel-default">
                  <div className="panel-heading">
                    <h4 className="panel-title">
                      <a data-toggle="collapse" data-parent="#accordion" href={`#${ids}${i}`}>{data.metadata.plugin_name}</a>
                    </h4>
                  </div>
                  <div id={`${ids}${i}`} className={'panel-body panel-collapse collapse panel-body-container container-box ' + (i === 0 ? 'in': '')}>
                    <Form schema={data.action_schema.schema} uiSchema={data.action_schema.uiSchema} onSubmit={log('submitted', data.action_schema.method, data.metadata.endpoint)} onError={log('errors'), false} />
                  </div>
                </div>
              )
          }
        }
      });
    }

    if(validateWidgetsToShow) {
      EdInActions.setClassWidth(validateWidgetsToShow);
    }

    return(
      validateWidgetsToShow ? (
        <div className="col-md-4 col-md-offset-1 margin-up-down spot-frame">
          <p><strong>Note:</strong> This is only an experimental plugin, it may work... sometimes.</p>
          <div className="panel-group overflowing" id="accordion">
            {plugins}
          </div>
        </div>
      ) : <div></div>
    );

  },
  callMethod: function(callback, endpoint, obj) {
    WidgetRequestStore.endPoint = endpoint;
    WidgetRequestStore.query = callback;
    WidgetRequestStore.ip = document.getElementById('dstIp').value || document.getElementById('query').value || '';
    WidgetRequestStore.formData = obj.formData;

    if(WidgetRequestStore.ip) {
      EdInActions.sendWidgetMethodData();
    } else {
      swal('Warning', 'Be sure to select at least a source/destination IP', 'warning');
    }
  },
  makeMenu: function(obj) {
    let indexMenu = SpotUtils.findObjArray(Menu.menu, 'labelledby', 'pluginsMenu');
    Menu.menu[indexMenu].sub.push({name: obj.name, link: '../../plugins/' + obj.link + '#date=${date}', target: '_blank'});
    EdInActions.changeMenu();
  },
  _onChange: function() {
    let data = WidgetFormStore.getData();
    let requests = WidgetRequestStore.getData();
    this.setState({data, requests});
  }
});

module.exports = WidgetController;

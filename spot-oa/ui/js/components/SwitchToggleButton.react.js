// Licensed to the Apache Software Foundation (ASF) under one or more contributor license agreements; and to You under the Apache License, Version 2.0.

var React = require('react');

var SwitchToggleButton = React.createClass({
  getInitialState: function () {
    return {
      isChecked: null
    };
  },
  componentWillMount () {
    this.setState({ isChecked: this.props.isChecked });
  },
  render () {

    return(
      <div className="switch-container">
        <label>
          <input ref="switch" checked={ this.state.isChecked } onChange={ this._handleChange } className="switch" type="checkbox" />
          <div>
            <span><g className="icon icon-toolbar grid-view"></g></span>
            <span><g className="icon icon-toolbar ticket-view"></g></span>
            <div></div>
          </div>
        </label>
      </div>
    );
  },
  _handleChange () {
    this.setState({isChecked: !this.state.isChecked});
    this.props.onChange(this.props.name, !this.state.isChecked);
  }
});


module.exports = SwitchToggleButton;

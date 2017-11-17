import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import {Layout, Menu , Carousel} from 'antd';
const {Header, Content, Footer} = Layout

export default class App extends Component {
  render() {
    return (
      <Layout className='Layout'>
        <Header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </Header>
        <Content className='Content'>
          <div style={{ background: 'lavender', opacity: 1}}>
            <video id='xpc_video' src="http://qiniu-video5.vmoviercdn.com/59f6a61b40879.mp4" autoplay='autoplay' controls='controls' loop='loop'>
            </video>
          </div>
        </Content>
        <Footer className='Footer'>
          Copyright ©2017 Created by Minokun
        </Footer>
      </Layout>
    );
  }
}
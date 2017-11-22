import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import {Layout, Row, Col, Carousel} from 'antd';
const {Header, Content, Footer} = Layout

class App extends Component {
  render() {
    return (
      <Layout className='Layout'>
        <Header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Minokun 数据站</h1>
        </Header>
        <Content className='Content'>
          <div className='video-div'>
            <div className='cover'>
              <div><h1 className='cover-word'>从数据中发现真理</h1></div>
              <div><h1 className='cover-word'>从真理中窥探未来</h1></div>
              <div><h1 className='cover-word'>大数据 + AI = Future</h1></div>
            </div>
            <video className='video-part' src='//qiniu-video5.vmoviercdn.com/59f6a61b40879.mp4' autoplay='autoplay' loop='loop'>
            </video>
            
          </div>
        </Content>
        <Footer className='Footer'>
          <Row>
          <Col span={8}>
          </Col>
          <Col span={8}>
          <p>
          <span className='icon-link'><img className='icon-img' alt='图片无法加载' src="http://echarts.baidu.com/images/icon-email.png" /></span>
          <span className='icon-link'><img className='icon-img' alt='图片无法加载' src="http://echarts.baidu.com/images/icon-weibo.png" /></span>
          <span className='icon-link'><img className='icon-img' alt='图片无法加载' src="http://echarts.baidu.com/images/icon-github.png" /></span>
          <span className='icon-link'><img className='icon-img' alt='图片无法加载' src="http://echarts.baidu.com/images/icon-twitter.png" /></span>
          </p>
          <p>Copyright ©2017 Created by Minokun</p>
            <span><img alt='图片无法加载' src='https://gw.alicdn.com/tfs/TB1GxwdSXXXXXa.aXXXXXXXXXXX-65-70.gif' className='bn_pic'/></span>
            <span><img alt='图片无法加载' style={{width:'20px', marginRight:'3px'}} src='https://img.alicdn.com/tfs/TB1..50QpXXXXX7XpXXXXXXXXXX-40-40.png'/></span>
            <span>版权所有ICP证：陇ICP备17000649号</span>
          <p>域名所属注册机构: HICHINA ZHICHENG TECHNOLOGY LTE</p>
          </Col>
          <Col span={8}>
          </Col>
          </Row>
        </Footer>
      </Layout>
    );
  }
}

export default App;

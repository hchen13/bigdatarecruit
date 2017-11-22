import React, { Component } from 'react';
import { Card } from 'antd';
import './Carousel.css';

export default class Hello extends Component {
	
	render() {
		return (
		  <Card style={{ width: 300 ,background:'red'}}>
		    <p>Card content</p>
		    <p>Card content</p>
		    <p>Card content</p>
		  </Card>
		);
	}
}
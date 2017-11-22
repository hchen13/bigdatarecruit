import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import Hello from './milk/Carousel.js';
import registerServiceWorker from './registerServiceWorker';
import {BrowserRouter as Router, Route} from 'react-router-dom';

class Homepage extends Component {
	render() {
		return(
			<Router>
				<div>
					<Route exact path="/" component={App}/>
                	<Route path="/hello" component={Hello}/>
				</div>
			</Router>
		);
	}
}

ReactDOM.render(<Homepage />, document.getElementById('root'));
registerServiceWorker();

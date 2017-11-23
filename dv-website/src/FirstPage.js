import React, { Component } from 'react';
import './FirstPage.css';
import { Carousel, Timeline, Icon, Row, Col, Card} from 'antd';

class FirstPage extends Component {
	render() {
		return (
			<div>
				<div className='video-div'>

		            <div className='cover'>
		              <div><h1 className='cover-word'>从数据中发现真理</h1></div>
		              <div><h1 className='cover-word'>从真理中窥探未来</h1></div>
		              <div><h1 className='cover-word'>大数据 + AI = Future</h1></div>
		            </div>

		            <video className='video-part' 
		              src='//qiniu-video5.vmoviercdn.com/59f6a61b40879.mp4' 
		              autoplay='autoplay' loop='loop' muted='muted'>
		            </video>

		            <Carousel autoplay slidesToShow='3' speed='800' centerMode='ture'>
		              <div className='carousel-label'>
		                <video className='video-label' 
		                  src='//qiniu-xpc5.vmoviercdn.com/59fbdd56ccd69.mp4' 
		                  poster='https://cs.vmovier.com/Uploads/avatar/2017/11/03/south.jpg@960w_540h_1e_1c.jpg' 
		                  controls='controls'>
		                </video>
		              </div>
		              <div className='carousel-label'>
		                <video className='video-label' 
		                  src='//qiniu-video3.vmoviercdn.com/5a01791ec8bf6.mp4' 
		                  poster='https://cs.vmovier.com/Uploads/avatar/2017/11/07/%E7%A5%9E%E5%A5%87%E7%9A%84%E6%8C%AA%E5%A8%81.jpg@960w_540h_1e_1c.jpg' 
		                  controls='controls'>
		                </video>
		              </div>
		              <div className='carousel-label'>
		                <video className='video-label' 
		                  src='//qiniu-xpc5.vmoviercdn.com/59ed5a426cb29.mp4' 
		                  poster='https://cs.vmovier.com/Uploads/avatar/2017/10/23/59e7819cacc69.jpeg@960w_540h_1e_1c.jpg@960w_540h_1e_1c.jpg' 
		                  controls='controls'>
		                </video>
		              </div>
		              <div className='carousel-label'>
		                <video className='video-label' 
		                  src='//qiniu-video5.vmoviercdn.com/59f3d3fe2bcdb.mp4' 
		                  poster='https://cs.vmovier.com/Uploads/avatar/2017/10/28/TIM20171028084559.jpg@960w_540h_1e_1c.jpg' 
		                  controls='controls'>
		                </video>
		              </div>
		              <div className='carousel-label'>
		                <video className='video-label' 
		                  src='//qiniu-video3.vmoviercdn.com/59f06c1e5f644.mp4' 
		                  poster='https://cs.vmovier.com/Uploads/avatar/2017/10/25/%E6%B2%99%E6%BC%A0%E9%9B%A81.jpg@960w_540h_1e_1c.jpg' 
		                  controls='controls'>
		                </video>
		              </div>
		              <div className='carousel-label'>
		                <video className='video-label' 
		                  src='//qiniu-xpc3.vmoviercdn.com/598afa96ac502.mp4' 
		                  poster='https://cs.vmovier.com/Uploads/cover/2017-05-11/59143a27a99f2_cut.jpeg@960w_540h_1e_1c.jpg' 
		                  controls='controls'>
		                </video>
		              </div>
		            </Carousel>
		        </div>

		        <Row className='time-line-div'>
		        <Col span={6}>
		        </Col>
		        <Col span={12}>

			        <div style={{background:'lavender', height:'100px'}}>
			        </div>
		        	<Row gutter={16} className='human-card'>
		        		<Col span={8}>
		        			<Card style={{ width: 240 }} bodyStyle={{ padding: 0 }}>
							    <div className="custom-image">
							      <img alt="example" width="100%" src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png" />
							    </div>
							    <div className="custom-card">
							      <h3>Europe Street beat</h3>
							      <p>www.instagram.com</p>
							    </div>
							  </Card>
		        		</Col>
		        		<Col span={8}>
		        			<Card style={{ width: 240 }} bodyStyle={{ padding: 0 }}>
							    <div className="custom-image">
							      <img alt="example" width="100%" src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png" />
							    </div>
							    <div className="custom-card">
							      <h3>Europe Street beat</h3>
							      <p>www.instagram.com</p>
							    </div>
							  </Card>
		        		</Col>
		        		<Col span={8}>
		        			<Card style={{ width: 240 }} bodyStyle={{ padding: 0 }}>
							    <div className="custom-image">
							      <img alt="example" width="100%" src="https://os.alipayobjects.com/rmsportal/QBnOOoLaAfKPirc.png" />
							    </div>
							    <div className="custom-card">
							      <h3>Europe Street beat</h3>
							      <p>www.instagram.com</p>
							    </div>
							  </Card>
		        		</Col>
		        	</Row>
					<Timeline className='time-line'>
						<Timeline.Item>Create a services site 2015-09-01</Timeline.Item>
						<Timeline.Item>Solve initial network problems 2015-09-01</Timeline.Item>
						<Timeline.Item dot={<Icon type="clock-circle-o" style={{ fontSize: '16px' }} />} color="red">Technical testing 2015-09-01</Timeline.Item>
						<Timeline.Item>Network problems being solved 2015-09-01</Timeline.Item>
					</Timeline>
				</Col>
		        <Col span={6}>
		        </Col>
				</Row>
		    </div>
		);
	}
}

export default FirstPage;
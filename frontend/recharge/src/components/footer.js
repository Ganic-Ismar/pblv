import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

const Footer = () => {
    return (
        <footer className="footer">
            <Container>
                <Row>
                    <Col md={6}>
                        <p>© 2024. Recharge</p>
                    </Col>
                </Row>
            </Container>
        </footer>
    );
};

export default Footer;

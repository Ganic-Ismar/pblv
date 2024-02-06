import React from 'react';
import Header from '../components/header';
import Footer from '../components/footer';
import Container from 'react-bootstrap/Container';

const Plan = () => {
    return (
        <div>
            <Container className='p-3'>
                <h1>Welcome to the Plan Page</h1>
                <p>This is the content of the plan page.</p>
            </Container>
            <Footer />
        </div>
    );
};

export default Plan;
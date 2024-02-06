import React from 'react';
import Header from '../components/header';
import Footer from '../components/footer';
import Container from 'react-bootstrap/Container';

const Home = () => {
    return (
        <div>
            <Header />
            <Container className='p-3'>
                <h1>Welcome to the Home Page</h1>
                <p>This is the content of the home page.</p>
            </Container>
            <Footer />
        </div>
    );
};

export default Home;

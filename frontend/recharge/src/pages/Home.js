import React from 'react';
import Header from '../components/header';
import Footer from '../components/footer';
import {render} from 'react-dom';
import Container from 'react-bootstrap/Container';
import DisplayChargingplan from '../components/DisplayCharingplan';
import ChargingplanProvider from '../context/chargingplanProvider';

const Home = () => {
    return (
        <div>
            <Container className='p-3'>
                <h1>Willkommen bei SmartCharge</h1>
                <ChargingplanProvider>
                    <DisplayChargingplan />
                </ChargingplanProvider>
            </Container>
            <Footer />
        </div>
    );
};

export default Home;

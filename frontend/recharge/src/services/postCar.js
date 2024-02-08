import Car from '../objects/Car.obj.js';

function postCar(car) {
    // Make a POST request to the server with the car data
    const api_host = process.env.REACT_APP_API_HOST;
    const api_port = process.env.REACT_APP_API_PORT;
    console.log(car)
    fetch('http://'+api_host+':'+api_port+'/cars/car', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(car)
    })
        .then(response => response.json())
        .then(data => {
            // Handle the response from the server
            console.log('Car posted successfully:', data);
        })
        .catch(error => {
            // Handle any errors that occur during the request
            console.error('Error posting car:', error);
        });
}

export default postCar;
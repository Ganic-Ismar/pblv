export async function fetchPlanData() {
    const response = await fetch('https://jsonplaceholder.typicode.com/comments');
    const data = await response.json();
    return data;
}

export async function fetchCarData() {
    const api_host = process.env.REACT_APP_API_HOST;
    const api_port = process.env.REACT_APP_API_PORT;
    const response = await fetch('http://'+api_host+':'+api_port+'/cars/cars');
    const data = await response.json();
    return data;
}
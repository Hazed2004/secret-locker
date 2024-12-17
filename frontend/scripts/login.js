import { API_ROOT_URL, LOGIN_ROUTE } from './constants.js';
import { getLocalStorageItem, setLocalStorageItem, elementManipulationERROR } from './common.js';

const token = getLocalStorageItem('token');
    if (token) {
    window.location.href = '/home';
}

document.getElementById('loginButton').addEventListener('click', async function(event) {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username.length < 1){
        elementManipulationERROR('alert', 'Invalid Username');
        return;
    }

    else if (password.length < 8){
        elementManipulationERROR('alert', 'Invalid Password');
        return;
    }

    const loginDetails = {
        username: username,
        password: password
    };
    
    try {
        const response = await axios.post(API_ROOT_URL + LOGIN_ROUTE, loginDetails);
        const token = response.data.token;
        setLocalStorageItem('token', token);
        window.location.href = '/home';
    } catch (error) {
        const errMsg = error.response.data.detail[0].msg;
        elementManipulationERROR('alert', errMsg);
    }
});

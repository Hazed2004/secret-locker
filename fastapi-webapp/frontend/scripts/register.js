import { API_ROOT_URL, REGISTER_ROUTE } from './constants.js';
import { getLocalStorageItem, setLocalStorageItem, elementManipulationERROR } from './common.js';

const token = getLocalStorageItem('token');
    if (token) {
    window.location.href = '/home';
}

document.getElementById('registerButton').addEventListener('click', async function(event) {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const passwordC = document.getElementById('passwordC').value;

    if (username.length < 1){
        elementManipulationERROR('alert', 'Invalid Username');
        return;
    }

    else if (password.length < 8){
        elementManipulationERROR('alert', 'Password should be atlease 8 characters');
        return;
    }

    else if (password != passwordC){
        elementManipulationERROR('alert', 'Password doesn\'t match Confirm Password');
        return;
    }

    const RegisterDetails = {
        username: username,
        password: password
    };

    try {
        const response = await axios.post(API_ROOT_URL + REGISTER_ROUTE, RegisterDetails);
        const token = response.data.token;
        setLocalStorageItem('token', token);
        window.location.href = '/home';
    } catch (error) {
        const errMsg = error.response.data.detail[0].msg;
        elementManipulationERROR('alert', errMsg);
    }
});

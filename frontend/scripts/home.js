import { API_ROOT_URL, USER_DATA_ROUTE, ADD_SECRET_ROUTE, DELETE_SECRET_ROUTE } from './constants.js'
import { getLocalStorageItem, verifyAuth, requestWtoken, elementManipulationTXT, elementManipulationERROR, sendRequestWithTokenAndData } from './common.js';

verifyAuth();
const token = getLocalStorageItem('token');
const data = await requestWtoken(API_ROOT_URL + USER_DATA_ROUTE, token);
const parsedData = JSON.parse(data);
elementManipulationTXT('main-content', "Your Secret: " + parsedData.secret);

document.getElementById('savebtn').addEventListener('click', async function(event) {
    const secret_value = document.getElementById('secretinput').value;
    if (secret_value.length < 1){
        elementManipulationERROR('alert', 'Enter Secret');
        return;
    }

    console.log(secret_value);
    const data = await sendRequestWithTokenAndData(API_ROOT_URL + ADD_SECRET_ROUTE, token, secret_value);
    alert("Your secret is saved");
    location.reload(true);

});

document.getElementById('deletebtn').addEventListener('click', async function(event) {
    requestWtoken(API_ROOT_URL + DELETE_SECRET_ROUTE, token)
    alert("Deleted your secret");
    location.reload(true);
});
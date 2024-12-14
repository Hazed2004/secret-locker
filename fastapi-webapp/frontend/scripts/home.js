import { API_ROOT_URL, USER_DATA_ROUTE } from './constants.js'
import { getLocalStorageItem, verifyAuth, requestWtoken, elementManipulationTXT } from './common.js';

verifyAuth();
const token = getLocalStorageItem('token');
const data = await requestWtoken(API_ROOT_URL + USER_DATA_ROUTE, token);
elementManipulationTXT('main-content', data);
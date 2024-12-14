export function verifyAuth() {
    const token = getLocalStorageItem('token');
    if (!token) {
        window.location.href = '/auth/login';
    }
}

export function setLocalStorageItem(name, value) {
    localStorage.setItem(name, value);
}

export function getLocalStorageItem(name) {
    return localStorage.getItem(name);
}

export async function requestWtoken(url, token) {
    try {
        const response = await axios.get(url, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        return JSON.stringify(response.data);
    } catch (error) {
        console.error('Request failed', error);
    }
}

export function elementManipulationTXT(eleid, content) {
    document.getElementById(eleid).innerText = content;
}

export function elementManipulationHTML(eleid, content) {
    document.getElementById(eleid).innerHTML = content;
}

export function elementManipulationERROR(eleid, content) {
    const element = document.getElementById(eleid);
    element.innerHTML = `
    <div role="alert" class="alert alert-error p-2 text-sm flex items-center">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-4 w-4 shrink-0 stroke-current"
          fill="none"
          viewBox="0 0 24 24">
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span class="text-grey">` + content + `</span>
    </div>`;
    setTimeout(() => {
        element.innerHTML = '';
    }, 2000);
}

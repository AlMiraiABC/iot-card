/**
 *
 * @param {string} key
 * @param {string} value
 * @param {number} maxAge seconds
 */
function addCookie(key, value, maxAge = 3600) {
    document.cookie = `${key}=${value};max-age=${maxAge};`;
}

/**
 *
 * @param {string} key
 */
function delCookie(key) {
    document.cookie = `${key}=;mag-age=-1;`;
}

/**
 *
 * @param {string} key
 * @returns Value of {@link key} if exists, otherwise empty string.
 */
function getCookie(key) {
    const found = document.cookie.split(';')
        .find(
            cookie => cookie.trim()
            .indexOf(`${key}=`) === 0
        );
    return found ? found.substring(key.length + 1, found.trim().length) : ''
}

/**
 * Check response.success
 * @param {Response} resp response
 * @returns {Object} response.data if success
 */
const _check_data = async(resp) => {
    const d = await resp.json();
    if (d.success) {
        return d.data;
    }
    return Promise.reject(d);
}

/**
 * Send a post request to {@link url} and serialize {@link data} to JSON as body with header `content-type: application/json`.
 * @param {string} url
 * @param {Object|null} data Request body
 * @returns
 */
const req_post = async(url, data) => {
    const resp = await fetch(
        url, {
            method: 'get',
            body: data ? JSON.stringify(data) : null,
            mode: 'cors',
            redirect: 'follow',
            headers: {
                'content-type': 'application/json'
            }
        }
    )
    return _check_data(resp);
}

/**
 * Send a get request to {@link url} and append {@link params} to url.
 * @param {string} url URL.
 * @param {Object} params Query parameters. A key-value dictionary.
 * @returns
 */
const req_get = async(url, params) => {
    if (params) {
        const qa = [];
        for (const key in params) {
            if (Object.hasOwnProperty.call(params, key)) {
                const value = params[key];
                qa.push(`${key}=${encodeURI(value)}`);
            }
        }
        if (url.indexOf('?') !== -1) {
            url = `${url}&${qa.join('&')}`;
        } else {
            url = `${url}?${qa.join('&')}`;
        }
    }
    const resp = await fetch(
        url, {
            method: 'get',
            redirect: 'follow',
        }
    )
    return _check_data(resp);
}

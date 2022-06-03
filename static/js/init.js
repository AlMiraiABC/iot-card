/**
 * Generate a random string
 * @param {number} length of result
 * @returns {string} random string.
 */
const genSalt = (length = 20) => {
    let chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^.-_';
    let str = '';
    for (let i = 0; i < length; i++) {
        str += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return str;
};
const appSaltElement = document.getElementById('app-salt');
document.getElementById('refresh-token').addEventListener('click', () => {
    appSaltElement.value = genSalt();
})
appSaltElement.value = genSalt();


const form = document.forms[0];
/**
 * Get form values.
 */
const getValues = () => {
    const manager = {
        email: form['account-email'].value,
        name: form['account-name'].value,
        password: form['account-password'].value
    };
    const server = {
        host: form['server-host'].value,
        userame: form['server-host'].value,
        passcode: form['server-passcode'].value,
        port: form['serer-port'].value,
        ssl: form['server-ssl'].checked
    };
    const sender = {
        email: form['sender-email'].value,
        name: form['sender-name'].value
    };
    const app = {
        salt: form['app-salt'].value,
        token_alg: form['app-alg'].value,
        login_exp: form['app-exp'].value,
        def_freq: form['app-freq'].value
    }
    for (const v of { ...manager, ...server, ...sender, ...app }) {
        if (v === null || v === undefined) {
            return;
        }
    }
    return { manager, server, sender, app };
};

document.getElementById('submit').addEventListener('click', () => {
    const data = getValues();
    if (!data) {
        return;
    }
    req_post('/init', data).then(_ => {
        window.location.href = '/manager.html';
    }).catch(err => {
        console.error(err);
    })
})

// init
const ps = new URLSearchParams(window.location.search)
const signin_tab = document.getElementById('tab-1');
const signup_tab = document.getElementById('tab-2');
const set_login = (signup) => {
    if (signup) {
        document.title = 'Sign up';
        signin_tab.removeAttribute('checked');
        signup_tab.setAttribute('checked', true);
        return;
    }
    document.title = 'Log in';
    signup_tab.removeAttribute('checked');
    signin_tab.setAttribute('checked', true);
}
set_login(ps.get('signup'));
// submit
const post_form = async (url, form) => {
    const resp = await fetch(url, {
        method: "POST",
        body: new FormData(form),
    });
    const d = await resp.json();
    if (d.success) {
        return d.data;
    }
    return Promise.reject(d);
}
/**
 * Show alert div.
 * @param {string|HTMLElement} element An alert div HTMLElement instance or it's id.
 * @param {string} msg Content of this alert div element.
 * @param {"primary"|"secondary"|"success"|"warning"|"danger"|"info"|"light"|"dark"} type Type of alert.
 */
const showAlert = (element, msg, type = 'success') => {
    if (typeof (element) === 'string') {
        element = document.getElementById(element);
    }
    if (element.nodeName !== 'DIV') {
        throw new TypeError('Element must be a DIV dom.');
    }
    if (!["primary", "secondary", "success", "warning", "danger", "info", "light", "dark"].find(t => t === type)) {
        throw new Error(`Parameter 'type' must be one of primary, secondary, success,warning, danger, info, light, dark, but got ${type}`);
    }
    type = type || 'success';
    const alertClasses = Array.from(element.classList).filter(c => c.startsWith('alert-'));
    element.classList.remove(...alertClasses);
    element.classList.add(`alert-${type}`);
    if (msg !== null && msg !== undefined) {
        element.innerText = msg;
    }
    element.removeAttribute('hidden');
}
const autoHideAlert = (element, msg, type, timeout = 3000) => {
    if (typeof (element) === 'string') {
        element = document.getElementById(element);
    }
    showAlert(element, msg, type);
    setTimeout(() => {
        element.setAttribute('hidden', '');
    }, timeout || 3000);
}
const si_form = document.forms['sign-in'];
const su_form = document.forms['sign-up'];
const alertElement = document.getElementById('result');

document.getElementById('si-submit').addEventListener('click', () => {
    if (!si_form.checkValidity()) {
        autoHideAlert(alertElement, 'Incorrect email or password.', 'danger');
        return;
    }
    post_form('/login', si_form).then(_ => {
        window.location.href = `./account.html`;
    }).catch(err => {
        console.error(err);
        autoHideAlert(alertElement, 'Incorrect email or password.', 'danger');
    });
});

const passwordAlertElement = document.getElementById('password-alert');
document.getElementById('su-submit').addEventListener('click', () => {
    if (!su_form.checkValidity()) {
        autoHideAlert(alertElement, 'Invalid email or password.', 'danger');
        return;
    }
    if (!passwordRobustness(su_form['password'].value)) {
        autoHideAlert(passwordAlertElement, undefined, 'danger', 5000);
        return;
    }
    post_form('/signup', su_form).then(_ => {
        window.location.href = `./account.html`;
    }).catch(err => {
        console.error(err);
        autoHideAlert(alertElement, 'Email is invalid or already exists. Plase input another one.');
    });
});

/**
 * Valid password format.
 * @param {string} password Password plain text to valid.
 * @param {number} len Minimum length of password.
 * @param {boolean} lower Contains at least one lower case english character.
 * @param {boolean} upper Contains at least one upper case english character.
 * @param {boolean} digest Contains at least one digest character.
 * @param {string} special Contains at least one special character.
 * @returns {boolean}
 */
const passwordRobustness = (password, len = 8, lower = true, upper = true, digest = true, special = '#?!@$ %^&*-') => {
    if (!password) {
        return false;
    }
    const pattern = new RegExp(`^${upper ? '(?=.*?[A-Z])' : ''}${lower ? '(?=.*?[a-z])' : ''}${digest ? '(?=.*?[0-9])' : ''}(?=.*?[${special || '#?!@$ %^&*-'}]).{${len || 8},}$`);
    return Boolean(password.match(pattern));
}

const logout = document.getElementById('logout');
if (logout) {
    logout.addEventListener('click', () => {
        req_post('/logout', null)
            .then(_ => null)
            .catch(_ => null);
        window.location.href = './login.html';
    });
}

const login = document.getElementById('login');
if (login) {
    login.addEventListener('click', _ => {
        window.location.href = './login.html';
    })
}
const signup = document.getElementById('signup');
if (signup) {
    signup.addEventListener('click', _ => {
        window.location.href = './login.html?signup=1';
    })
}

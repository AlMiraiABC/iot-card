req_post('/account/').then(info => {
    const name = document.getElementById('name');
    name.innerText = info.name;
    const email = document.getElementById('email')
    email.innerText = info.email;
    email.setAttribute('title', info.name);
    const cards = document.getElementById('cards');
    cards.innerHTML = cardTagHTML(info.cards);
    for (const cardTag of cards.getElementsByClassName('card-tag')) {
        cardTag.firstChild.addEventListener('click', (e) => {
            setDigest(e.target.innerText);
        })
        cardTag.lastChild.addEventListener('click', () => {
            // TODO: delete card.
        })
    }
}).catch((err) => {
    console.error(err);
    window.location.href = './login.html'
});

/**
 * Set card digest offcanvas.
 * @param {string} cardID ID of card.
 */
const setDigest = (cardID) => {
    const digestText = {
        'balance': { read: '余额', content: (d, _) => `￥${d.balance}` },
        'phone': { read: '手机号', content: (d, _) => d.phone },
        'isp': { read: '运营商', content: (d, _) => d.isp },
        'plan': { read: '套餐', content: (d, _) => d.plan },
        'status': { read: '网卡状态', content: (d, _) => d.status },
        'expired': { read: '过期时间', content: (d, _) => d.expired },
        'total': { read: '总流量', content: (d, _) => `${(d.total / 1024).toFixed(2)} GB (${d.total.toFixed(0)} MB)` },
        'usage': { read: '已用流量', content: (d, _) => `${(d.usage / 1024).toFixed(2)} GB (${d.usage.toFixed(0)} MB)` },
        'remain': { read: '剩余流量', content: (d, _) => `${((d.total - d.usage) / 1024).toFixed(2)} GB (${(d.total - d.usage).toFixed(0)} MB)` },
        'renew': { read: '次月', content: (d, _) => d.renew ? 'True' : 'False' },
    };
    const digest = document.getElementById('digest');
    digest.innerHTML = digestHTML(digestText);
    const iccid = document.getElementById('iccid');
    iccid.innerHTML = `<p class="col-7 placeholder placeholder-wave"></p>`;
    document.getElementById('card-id').innerText = cardID;
    req_get(`/query/${cardID}/digest`).then(d => {
        iccid.innerText = d.iccid;
        for (const id in digestText) {
            const element = document.getElementById(id);
            element.innerText = digestText[id].content(d, element);
        }
    });
}

/**
 * Generate digest modal HTML.
 * @param {{[id:string]:{read:string}}} digest
 * @returns {string}
 */
const digestHTML = (digest) => {
    let table = ''
    for (const id in digest) {
        table += `<tr>
                    <td>${digest[id].read}</td>
                    <td id="${id}">
                        <p class="col-7 placeholder placeholder-wave" style="width: 100px;">
                        </p>
                    </td>
                </tr>`;
    }
    return `<tbody>
                ${table}
            </tbody>`;
}

/**
 * Generate card tag HTML.
 * @param {string[]} cardIDs ID of cards.
 * @return {string}
 */
const cardTagHTML = (cardIDs) => {
    const cardTags = cardIDs.map(cardID => `
                    <div class="card-tag">
                        <button type="button" class="btn btn-link" data-bs-toggle="offcanvas" data-bs-target="#card-digest" aria-controls="card-digest">
                            ${cardID}
                        </button>
                        <button type="button" class="btn">
                            <i class="bi bi-x-lg"></i>
                        </button>
                    </div>`)
    return `<div class="btn-group" role="group">
                ${cardTags.join('')}
            </div>`
}

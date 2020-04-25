function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


let cart = [];


function setCart(newCart) {
    cart = newCart;
    let total = 0;
    cart.forEach(order_item => total += order_item.item.price * order_item.quantity);
    total = Math.round(total * 10) / 10;
    divCart = cart.map(order_item => `
    <div class="item py-2">
    <button onclick="removeItem(${ order_item.item.id})" type="button" class="close">×</button>
    <div class="row m-0">
        <div class="col-3 d-flex justify-content-center align-items-start">
            <img  style="height: auto;max-width: 100%;max-height: 6rem;"
                src="${ order_item.item.photo}">
        </div>
        <div class="col-9 p-0">
            <h6>${ order_item.item.title}</h6>
            <p><small>${order_item.item.size ? `${order_item.item.size} см, ${order_item.item.description}` : order_item.item.description}</small></p>
            <div class="row p-0">
                <div class="col">
                    <div class="input-group input-spinner" style="width: 5.5rem;">
                        <button
                            onclick="updateItem(${ order_item.item.id}, ${order_item.quantity} + 1)"
                            class="btn btn-outline-primary p-0 d-flex justify-content-center align-items-center"
                            type="button" id="button-plus"
                            style="	border-top-left-radius: 20px;	border-bottom-left-radius: 20px;	width: 30px;	height: 30px;">+</button>
                        
                        <div class="form-control p-0 text-center border-primary border" style="height: 30px;outline:none;border:1px solid inherit">
                            ${ order_item.quantity}
                        </div>
                        <button
                            onclick="updateItem(${ order_item.item.id}, ${order_item.quantity} - 1)"
                            class="btn btn-outline-primary p-0 d-flex justify-content-center align-items-center flex-grow-0"
                            type="button" id="button-minus"
                            style="	border-top-right-radius: 20px;	border-bottom-right-radius: 20px;	width: 30px;	height: 30px;">−</button>
                    </div>
                </div>
                <div class="col text-right">
                    <p>${ order_item.item.price} руб.</p>
                </div>
            </div>
        </div>
    </div>
</div>
    `).join('');
    if (total == 0) {
        divCart += `
        <div class="text-center">
        <img src="/static/images/pizza.gif" alt="" style="width: 18rem;">
        <h4>Корзина пуста</h4>
    </div>
    </div>
        `
    } else {
        divCart += `
    <div class="dropdown-divider"></div>
    <div class="row">
        <div class="col"> Сумма заказа </div>
        <div class="col text-right"> ${total} руб.</div>
    </div>
    </div>
    `
    }

    Array.from(document.getElementsByClassName('cart')).forEach(cart => cart.innerHTML = divCart);
}


function getItems() {
    fetch('api/cart').then(response => response.json()).then(cart => setCart(cart))
}


function addItem(id) {
    const item = cart.find(order_item => order_item.item.id == id);
    if (item) {
        updateItem(id, item.quantity + 1)
    } else {
        fetch(`api/cart/${id}`, {
            method: "post",
            credentials: "same-origin",
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            }
        }).then(response => response.json()).then(order_item => setCart([...cart, order_item]))
    }
}


function updateItem(id, quantity) {
    if (quantity == 0)
        removeItem(id)
    else {
        const order_item = cart.find(order_item => order_item.item.id == id)
        fetch(`api/cart/${id}`, {
            method: "put",
            credentials: "same-origin",
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                item: order_item['item'],
                quantity
            })
        }).then(response => {
            if (response.ok) {
                setCart(cart.map(order_item => {
                    if (order_item.item.id == id)
                        order_item.quantity = quantity
                    return order_item
                }))
            }
        })
    }
}


function removeItem(id) {
    fetch(`api/cart/${id}`, {
        method: "delete",
        credentials: "same-origin",
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': csrftoken,
        }
    }).then(response => {
        if (response.ok)
            setCart(cart.filter(order_item => order_item.item.id !== id))
    }
    )
}


window.onload = getItems;

function toggleDropdown(e) {
    const _d = $(e.target).closest('.dropdown');
    const _m = $('.dropdown-menu', _d);
    setTimeout(function () {
        const shouldOpen = e.type !== 'click' && _d.is(':hover');
        _m.toggleClass('show', shouldOpen);
        _d.toggleClass('show', shouldOpen);
        $('[data-toggle="dropdown"]', _d).attr('aria-expanded', shouldOpen);
    }, e.type === 'mouseleave' ? 1000 : 0);
}

$('body')
    .on('mouseenter mouseleave', '.dropdown', toggleDropdown)
    .on('click', '.dropdown-menu a', toggleDropdown);
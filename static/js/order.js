function setModal(text) {
    let modal = document.getElementById('modal');
    modal.innerHTML = `
        <div class="row">
            <div class="col d-flex justify-content-center">
                <h3>${text}</h3>
            </div>     
        </div>
    `
}


function order(street, house, apartment, email, order_time) {
    fetch('http://127.0.0.1:8000/order', {
        method: "post",
        credentials: "same-origin",
        headers: {
            'Content-type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            street,
            house,
            apartment,
            email,
            order_time
        })
    }).then(response => response.json()).then(text => setModal(text))
}


carryout.onsubmit = async (e) => {
    e.preventDefault();
    const restaurant = document.getElementById('restaurant');
    select = restaurant.options[restaurant.selectedIndex];
    street = select.getAttribute('street');
    house = select.getAttribute('house');
    apartment = select.getAttribute('apartment');
    form = new FormData(carryout);
    email = form.get('email');
    order_time = form.get('order_time');
    order(street, house, apartment, email, order_time);
}


delivery.onsubmit = async (e) => {
    e.preventDefault();
    form = new FormData(delivery);
    street = form.get('street');
    house = form.get('house');
    apartment = form.get('apartment');
    email = form.get('email');
    order_time = form.get('order_time');
    order(street, house, apartment, email, order_time);
}
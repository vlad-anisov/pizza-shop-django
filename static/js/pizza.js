let items = [];
let item = {};


function setModal(number){
    item = items[number];
    document.getElementById('modalPhoto').innerHTML = `
        <img class="card-img-top"
            src="${item.photo}" alt="Card image cap" style="width:18rem;">
    `
    document.getElementById('modalDescription').innerHTML = `
            <h3>${item.title}</h3>
            <p>${item.description}</p>
            <p style="line-height: 1;"><small class="p-0">Пищевая ценность на 100г продукта:<br>
                Жиры - ${item.fats} г<br>
                Белки - ${item.fats} г<br>
                Углеводы - ${item.fats} г<br>
                Энергетическая ценность - ${item.fats} ккал.</small></p>
            <p>Вес ${item.weight} г</p>
    `
    document.getElementById('modalPrice').innerHTML = `
                <button class="btn btn-primary mt-4" data-dismiss="modal" style="width: 18rem;" onclick="addItem(${item.id})">
                    Добавить в корзину за ${item.price} руб.
                </button>
    `
}


function modal(button) {
    fetch(`api/pizza/${button.id}`)
        .then(response => response.json()).then(pizza => {
            items = pizza;
            document.getElementById('modalSelect').innerHTML = `
                <div class="btn-group btn-group-toggle" data-toggle="buttons">
                    <label class="btn btn-outline-primary active" style="width: 6rem;">
                        <input type="radio" onchange="setModal(0)" name="options" checked>25 см
                    </label>
                    <label class="btn btn-outline-primary" style="width: 6rem;">
                        <input type="radio" onchange="setModal(1)" name="options">30 см
                    </label>
                    <label class="btn btn-outline-primary" style="width: 6rem;">
                        <input type="radio" onchange="setModal(2)" name="options">35 см
                    </label>
                </div>
            `
            setModal(0);
        })
}


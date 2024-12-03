document.addEventListener('DOMContentLoaded', function () {
    const user = localStorage.getItem('user');
    document.getElementById('user').textContent = user ? user : '';
    document.getElementById('logoutButton').addEventListener('click', function () {
        localStorage.removeItem('user');
        window.location.href = '/home';
});

document.getElementById('check_price').addEventListener('click', showCheckPrice);
document.getElementById('start_sell').addEventListener('click', showSell);
document.getElementById('cancel_item').addEventListener('click', cancelItem);
document.getElementById('close_cash_register').addEventListener('click', showCloseCashRegister);
    
document.addEventListener('keydown', function(event) {
    if (event.key === 'F') showCheckPrice();
    if (event.key === 'V') showSell();
    if (event.key === 'C') cancelItem();
    if (event.key === 'Ç') showCloseCashRegister();
});

function showCheckPrice() {
    hideAllSections();
    document.querySelector('.check_price').style.display = 'block';
    clearInputAndFocus('#barcode_check');
}

function showSell() {
    hideAllSections();
    document.querySelector('.sell').style.display = 'block';
    clearInputAndFocus('#barcode');
}
    
function cancelItem() {
    alert("Cancelar item não implementado ainda!");
}

function showCloseCashRegister() {
    hideAllSections();
    document.querySelector('.close_cash_register').style.display = 'block';
}
    
function hideAllSections() {
    document.querySelectorAll('.check_price, .sell, .close_cash_register').forEach(function(section) {
        section.style.display = 'none';
    });
}

function clearInputAndFocus(selector) {
    const input = document.querySelector(selector);
    if (input) {
        input.value = '';
        input.focus();
    }
}

document.getElementById('check_price_button').addEventListener('click', function () {
    const barcode = document.getElementById('barcode_check').value;
    if (barcode) {
        document.getElementById('product-name').textContent = "Produto Exemplo";
        document.getElementById('price').textContent = "R$ 9,99";
    } else {
        alert("Código de barras não fornecido.");
    }
});

document.getElementById('add_item').addEventListener('click', function () {
    const quantity = parseInt(document.getElementById('quantity').value) || 1;
        const barcode = document.getElementById('barcode').value;

    if (barcode) {
        const itemName = "Produto Exemplo";
        const unitPrice = 9.99;
        const totalItem = unitPrice * quantity;
    
        document.getElementById('product-name').textContent = itemName;
        document.getElementById('unit-price').textContent = `R$ ${unitPrice.toFixed(2)}`;
        document.getElementById('total-item').textContent = `R$ ${totalItem.toFixed(2)}`;
        document.getElementById('items-on-cart').textContent += `${itemName} x ${quantity} - R$ ${totalItem.toFixed(2)}\n`;
    
        let subtotal = parseFloat(document.getElementById('subtotal').textContent.replace("R$ ", "")) || 0;
        subtotal += totalItem;
        document.getElementById('subtotal').textContent = `R$ ${subtotal.toFixed(2)}`;
        document.getElementById('total-sell').textContent = `R$ ${subtotal.toFixed(2)}`;
    } else {
        alert("Código de barras não fornecido.");
    }
});
    
document.getElementById('card').addEventListener('click', function () {
    showPaymentOptions(['card1', 'card2', 'card3']);
});

document.getElementById('money').addEventListener('click', function () {
    showPaymentOptions(['money1', 'pix']);
});

function showPaymentOptions(options) {
    hideAllPayments();
    options.forEach(optionId => {
        document.getElementById(optionId).style.display = 'inline';
    });
    document.getElementById('to_pay').style.display = 'block';
}

function hideAllPayments() {
    document.querySelectorAll('#card1, #card2, #card3, #money1, #pix, #to_pay').forEach(function(element) {
        element.style.display = 'none';
    });
}

document.getElementById('paid').addEventListener('input', function () {
    const totalSell = parseFloat(document.getElementById('total-sell').textContent.replace("R$ ", "")) || 0;
    const paid = parseFloat(document.getElementById('paid').value) || 0;
    const leftToPay = Math.max(totalSell - paid, 0);
    document.getElementById('left-to-pay').textContent = `R$ ${leftToPay.toFixed(2)}`;
});
});
    
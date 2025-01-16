// Atualizar carrinho

document.addEventListener('DOMContentLoaded', () => {
    const updateCartButtons = document.querySelectorAll('.btn-update-cart');

    updateCartButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();

            const produtoId = button.getAttribute('data-produto-id');
            const acao = button.getAttribute('data-acao');

            fetch(updateCartUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: `produto_id=${produtoId}&acao=${acao}`
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro na requisição');
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    console.error(data.error);
                    return;
                }

                const quantidadeElement = document.querySelector(`tr[data-produto-id="${produtoId}"] .quantidade`);
                quantidadeElement.textContent = data.quantidade;

                const subtotalElement = document.querySelector(`tr[data-produto-id="${produtoId}"] .subtotal`);
                subtotalElement.textContent = `${data.subtotal.toFixed(2)}`;

                const totalElement = document.getElementById('cart-total');
                totalElement.textContent = `${data.total.toFixed(2)}`;
            })
            .catch(error => {
                console.error('Erro:', error);
            });
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});


// Mostrar o modal

document.addEventListener("DOMContentLoaded", () => {
    const loginLink = document.getElementById('login-modal');
    const closeModal = document.getElementById('close-modal');
    const modal = document.querySelector('.modal');
    const dropdownProfile = document.getElementById('profile-img');
    const closeDropdown = document.querySelector('.dropdown-menu');

    if (loginLink && modal) {
        loginLink.addEventListener('click', (event) => {
            event.preventDefault();
            modal.style.display = 'block';
        });
    }

    if (closeModal && modal) {
        closeModal.addEventListener('click', (event) => {
            event.preventDefault();
            modal.style.display = 'none';
        });
    }

    if (dropdownProfile && closeDropdown) {
        dropdownProfile.addEventListener('click', (event) => {
            event.preventDefault();
            closeDropdown.classList.toggle('visible');
        });
    }
});

// Mostrar o modal quando login invalido

function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

const loginError = getQueryParam('login_error');
if (loginError === 'true') {
    const modal = document.querySelector('.modal');
    modal.style.display = 'block';
}
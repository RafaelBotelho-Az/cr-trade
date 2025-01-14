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
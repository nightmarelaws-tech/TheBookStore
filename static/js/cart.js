// static/js/cart.js
// Handles all cart interactions:
// 1. Add to cart button (any page)
// 2. Quantity +/- buttons (cart page)
// 3. Remove item button (cart page)
// 4. Updates cart badge in navbar

$(function () {

    // ----- helper: read CSRF token from cookie -----
    function getCookie(name) {
        let value = '';
        document.cookie.split(';').forEach(function (c) {
            if (c.trim().startsWith(name + '=')) {
                value = decodeURIComponent(c.trim().slice(name.length + 1));
            }
        });
        return value;
    }

    // ----- helper: update the cart badge number in navbar -----
    function updateCartBadge(count) {
        const $badge = $('.cart-badge');
        if (count > 0) {
            if ($badge.length) {
                $badge.text(count);
            } else {
                $('.cart-nav-link').append(
                    '<span class="cart-badge">' + count + '</span>'
                );
            }
        } else {
            $badge.remove();
        }
    }

    // ----- helper: recalculate grand total on cart page -----
    function recalcTotal() {
        let total = 0;
        // loop through each cart row and add up subtotals
        $('.cart-item-row').each(function () {
            const unitPrice = parseFloat($(this).data('unit-price'));
            const qty       = parseInt($(this).find('.cart-qty-number').text());
            const subtotal  = unitPrice * qty;
            // update this row's subtotal display
            const itemId = $(this).attr('id').replace('cart-item-', '');
            $('#subtotal-' + itemId).text('€' + subtotal.toFixed(2));
            total += subtotal;
        });
        // update the grand total
        $('#cart-total').text('€' + total.toFixed(2));
        $('#cart-grand-total').text('€' + total.toFixed(2));
    }


    // ----- ADD TO CART -----
    // works on catalogue, homepage, book detail, dashboard
    $(document).on('click', '.btn-add-to-cart', function () {
        const $btn   = $(this);
        const bookId = $btn.data('book-id');

        $btn.prop('disabled', true).html(
            '<i class="bi bi-hourglass-split me-1"></i>Adding...'
        );

        $.ajax({
            url:     '/cart/add/' + bookId + '/',
            method:  'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            data:    { quantity: 1 },
            success: function (data) {
                if (data.success) {
                    updateCartBadge(data.cart_count);
                    $btn.html('<i class="bi bi-bag-check me-1"></i>Added!');
                    setTimeout(function () {
                        $btn.prop('disabled', false).html(
                            '<i class="bi bi-bag-plus me-1"></i>Add to Cart'
                        );
                    }, 2000);
                }
            },
            error: function () {
                $btn.prop('disabled', false).html(
                    '<i class="bi bi-bag-plus me-1"></i>Add to Cart'
                );
                alert('Please sign in to add items to cart.');
            }
        });
    });


    // ----- PLUS BUTTON on cart page -----
    $(document).on('click', '.btn-qty-plus', function () {
        const itemId  = $(this).data('item-id');
        const $qtyEl  = $('#qty-' + itemId);
        let   qty     = parseInt($qtyEl.text());
        qty++;
        $qtyEl.text(qty);

        // tell server about the new quantity
        $.ajax({
            url:     '/cart/update/' + itemId + '/',
            method:  'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            data:    { quantity: qty },
            success: function () {
                recalcTotal();
            }
        });
    });


    // ----- MINUS BUTTON on cart page -----
    $(document).on('click', '.btn-qty-minus', function () {
        const itemId  = $(this).data('item-id');
        const $qtyEl  = $('#qty-' + itemId);
        let   qty     = parseInt($qtyEl.text());

        if (qty <= 1) {
            // if quantity reaches 0 remove the item entirely
            removeCartItem(itemId);
            return;
        }

        qty--;
        $qtyEl.text(qty);

        $.ajax({
            url:     '/cart/update/' + itemId + '/',
            method:  'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            data:    { quantity: qty },
            success: function () {
                recalcTotal();
            }
        });
    });


    // ----- REMOVE ITEM BUTTON on cart page -----
    $(document).on('click', '.btn-remove-item', function () {
        const itemId = $(this).data('item-id');
        removeCartItem(itemId);
    });


    // ----- helper: remove a cart item row -----
    function removeCartItem(itemId) {
        $.ajax({
            url:     '/cart/remove/' + itemId + '/',
            method:  'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            success: function (data) {
                // fade out and remove the row from the page
                $('#cart-item-' + itemId).fadeOut(300, function () {
                    $(this).remove();
                    recalcTotal();
                    updateCartBadge(data.cart_count);

                    // if no more items show empty state message
                    if ($('.cart-item-row').length === 0) {
                        location.reload();
                    }
                });
            }
        });
    }

});
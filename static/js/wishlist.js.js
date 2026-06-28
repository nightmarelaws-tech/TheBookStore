// Handles adding and removing books from the wishlist
// Uses AJAX so page does not reload

$(function () {

    // ----- TOGGLE WISHLIST -----
    // works on any page that has a wishlist button
    $(document).on('click', '.btn-toggle-wishlist', function () {
        const $btn   = $(this);
        const bookId = $btn.data('book-id');
        const csrfToken = $('[name=csrfmiddlewaretoken]').val() ||
                          getCookie('csrftoken');

        $.ajax({
            url:    '/wishlist/toggle/' + bookId + '/',
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken },
            success: function (data) {
                if (data.added) {
                    // book was added to wishlist
                    $btn.html('<i class="bi bi-heart-fill me-2"></i>Saved');
                    $btn.addClass('active');
                } else {
                    // book was removed from wishlist
                    $btn.html('<i class="bi bi-heart me-2"></i>Save');
                    $btn.removeClass('active');
                }
            },
            error: function () {
                alert('Please sign in to use the wishlist.');
            }
        });
    });

    // ----- helper to read cookie by name -----
    // used to get the CSRF token Django sets in the browser
    function getCookie(name) {
        let value = '';
        document.cookie.split(';').forEach(function (c) {
            if (c.trim().startsWith(name + '=')) {
                value = decodeURIComponent(c.trim().slice(name.length + 1));
            }
        });
        return value;
    }

});
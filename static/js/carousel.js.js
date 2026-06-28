$(function () {

    // ----- only run if carousel exists on this page -----
    if ($('#booksTrack').length === 0) return;

    // current position of the carousel (which book index we are at)
    let currentIndex = 0;

    // count how many book items exist
    const $items     = $('.carousel-book-item');
    const totalItems = $items.length;

    // how many items visible at once depends on screen size
    function getVisibleCount() {
        if ($(window).width() < 576) return 2;   // mobile - 2 books
        if ($(window).width() < 992) return 3;   // tablet - 3 books
        return 5;                                  // desktop - 5 books
    }

    // ----- MOVE CAROUSEL -----
    // calculates how far to slide the track left
    function moveCarousel() {
        const itemWidth  = $items.first().outerWidth(true); // width including gap
        const moveAmount = currentIndex * itemWidth;
        // slide the track left by the correct amount
        $('#booksTrack').css('transform', 'translateX(-' + moveAmount + 'px)');
    }

    // ----- NEXT BUTTON -----
    $('#carouselNext').on('click', function () {
        const visible  = getVisibleCount();
        const maxIndex = totalItems - visible;

        if (currentIndex < maxIndex) {
            currentIndex++;  // move one book to the right
        } else {
            currentIndex = 0;  // loop back to start
        }
        moveCarousel();
    });

    // ----- PREV BUTTON -----
    $('#carouselPrev').on('click', function () {
        const visible  = getVisibleCount();
        const maxIndex = totalItems - visible;

        if (currentIndex > 0) {
            currentIndex--;  // move one book to the left
        } else {
            currentIndex = maxIndex;  // jump to end
        }
        moveCarousel();
    });

    // recalculate on window resize so mobile/desktop counts stay correct
    $(window).on('resize', function () {
        currentIndex = 0;  // reset to start on resize
        moveCarousel();
    });

});
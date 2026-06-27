/*
 * The Book Merchant - main.js
 * Runs on every page.
 * Handles: dark mode, flash message dismiss, back to top button*/

$(function () {

    /*1. DARK MODE-Saves user preference in localStorage so it remembers between page visits*/

    // Check if user had dark mode on from a previous visit
    const savedDark = localStorage.getItem('darkMode') === 'true';

    // Apply dark mode immediately on page load if saved
    if (savedDark) {
        $('body').addClass('dark-mode');
        // Change moon icon to sun icon
        $('#darkModeToggle i')
            .removeClass('bi-moon-fill')
            .addClass('bi-sun-fill');
    }

    // When user clicks the dark mode toggle button
    $('#darkModeToggle').on('click', function () {

        // Toggle the dark-mode class on body
        $('body').toggleClass('dark-mode');

        // Check if dark mode is now ON or OFF
        const isDark = $('body').hasClass('dark-mode');

        // Swap between moon and sun icon
        $('#darkModeToggle i')
            .toggleClass('bi-moon-fill', !isDark)
            .toggleClass('bi-sun-fill', isDark);

        // Save the new preference to localStorage
        localStorage.setItem('darkMode', isDark);
    });


    /* 2. FLASH MESSAGE AUTO DISMISS
       Django shows success/error messages - auto hide after 4 seconds*/
    const $alerts = $('.alert-dismissible');

    if ($alerts.length) {
        setTimeout(function () {
            // Fade out then remove from DOM
            $alerts.fadeOut(500, function () {
                $(this).remove();
            });
        }, 4000); // 4 seconds
    }


    /*
       3. BACK TO TOP BUTTON
       Shows after scrolling 300px, smooth scrolls back to top*/
    const $backToTop = $('#backToTop');

    // Show or hide button based on scroll position
    $(window).on('scroll', function () {
        if ($(this).scrollTop() > 300) {
            $backToTop.fadeIn(200);
        } else {
            $backToTop.fadeOut(200);
        }
    });

    // Smooth scroll to top when button is clicked
    $backToTop.on('click', function () {
        $('html, body').animate({ scrollTop: 0 }, 400);
    });


    /*4. ACTIVE NAV LINK- Highlights the correct nav link based on current page URL */
    const currentPath = window.location.pathname;

    // Loop through all nav links and check if they match current URL
    $('#mainNavbar .nav-link').each(function () {
        const linkPath = $(this).attr('href');

        // Mark as active if URL matches (but not just '/' for every page)
        if (linkPath && linkPath !== '/' && currentPath.startsWith(linkPath)) {
            $(this).addClass('active');
        } else if (linkPath === '/' && currentPath === '/') {
            $(this).addClass('active');
        }
    });

}); // end document ready
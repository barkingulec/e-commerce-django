
//$(window).scroll(function () {
//    var scroll = $(window).scrollTop();
//    if (scroll >= 0.4 * $(window).height()) {
//        $("#nav").addClass('fadeout');
//    } else {
//        $("#nav").removeClass('fadeout');
//    }
//});

//$(document).scroll(function () {
//    var scrollPos = $(this).scrollTop();
//    var transY = scrollPos / 4.6;
//    $('.home-section').css({
//        'background-position-y': `-${transY}px`,
//    });
//});

//$(document).scroll(function () {
//    var scrollPos = $(this).scrollTop();
//    $('.home-join-us, .home-products, .home-discuss').css({
//        'opacity': ((scrollPos - 600)/ 380),
//    });
//});



$(document).scroll(function () {
    var scrollPos = $(this).scrollTop();

    if (scrollPos > 500) {
        $('.home-first-h1').css({
            'top': '30%',
        });
        $('.home-second-h1').css({
            'opacity': 1,
        });
    }

    $('.home-h1').css({
        'opacity': 1 - ((scrollPos) / 250),
    });
    $('.home-h1-desc').css({
        'opacity': 1 - ((scrollPos - 250) / 350),
    });
    $('.bg1').css({
        'opacity': ((scrollPos - 800) / 500),
    });
    $('.bg2').css({
        'opacity': ((scrollPos - 1200) / 700),
    });
    $('.home-parallax-2').css({
        'opacity': ((scrollPos - 800) / 400),
    });
    $('.parallax-products').css({
        'opacity': ((scrollPos - 1700) / 400),
    });
    if (scrollPos > 1500) {
        $('.home-parallax-2').css({
            'opacity': 1 - ((scrollPos - 1500) / 300),
        });
    }
    if (scrollPos > 700) {
        $('.home-h1, .home-h1-desc').css({
            'left': '-50%',
        });
        $('.home-join-us').css({
            'left': '50%',
        });
        $('.home-products').css({
            'left': '30%',
        });
        $('.home-discuss').css({
            'left': '70%',
        });
    }
    if (scrollPos <= 700) {
        $('.home-h1, .home-h1-desc').css({
            'left': '50%',
        });
        $('.home-join-us, .home-products, .home-discuss').css({
            'left': '-20%',
        });
    }
    if (scrollPos > 1700) {
        $('.home-parallax-2').css({
            'left': '-50%',
        });
    }
    if (scrollPos >= 2700) {
        $('.parallax-products').css({
            'opacity': 1 - ((scrollPos - 2700) / 300),
        });
    }
    if (scrollPos >= 2900 || scrollPos < 2000) {
        $('.parallax-products').css({
            'left': '-110%',
        });
    }
    if (scrollPos < 2900 && scrollPos >= 2000) {
        $('.parallax-products').css({
            'left': '20%',
        });
    }
    if (scrollPos <= 2900) {
        $('.home-footer').css({
            'bottom': '-30%',
        });
    }
    var homeFooter = ((scrollPos - 2900) / 8) - 30
    if (scrollPos > 2900) {
        if (homeFooter > 0) { homeFooter = 0 };
        $('.home-footer').css({
            'bottom': `${homeFooter}%`,
        });
    }
});

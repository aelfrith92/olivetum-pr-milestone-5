/**
 * It adds the hovering effect to the shopping bag svg file, which cannot be styled via CSS
 */

$(document).ready(function () {
    // Self-invoking f for svg fills
    (function () {

        // Select the path tag inside the svg tag to modify its attribute 'stroke'
        $('#shoppingBagSvgHoverColor').mouseover(function (event) {
            event.stopPropagation();
            $('#shoppingBagSvgHoverColor path').attr('fill', '#181D31');
        });
        $('#shoppingBagSvgHoverColor').mouseleave(function (event) {
            event.stopPropagation();
            $('#shoppingBagSvgHoverColor path').attr('fill', '#f8f3e5');
        });

        $('#searchBtn').mouseover(function (event) {
            event.stopPropagation();
            $('#searchBtn path').attr('fill', '#181D31');
        });
        $('#searchBtn').mouseleave(function (event) {
            event.stopPropagation();
            $('#searchBtn path').attr('fill', '#f8f3e5');
        });
    })();

    (function ($) {
        window.fnames = new Array();
        window.ftypes = new Array();
        fnames[0] = 'EMAIL';
        ftypes[0] = 'email';
        fnames[1] = 'FNAME';
        ftypes[1] = 'text';
        fnames[2] = 'LNAME';
        ftypes[2] = 'text';
        fnames[3] = 'ADDRESS';
        ftypes[3] = 'address';
        fnames[4] = 'PHONE';
        ftypes[4] = 'phone';
        fnames[5] = 'BIRTHDAY';
        ftypes[5] = 'birthday';
    }(jQuery));
    var $mcj = jQuery.noConflict(true);
});
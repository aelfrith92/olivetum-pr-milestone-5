/**
* It adds the hovering effect to the shopping bag svg file, which cannot be styled via CSS
*/

$( document ).ready(function() {
    // Self-invoking f for svg fills
    (function () {
        
        // Select the path tag inside the svg tag to modify its attribute 'stroke'
        $('#shoppingBagSvgHoverColor').mouseover(function(event){
            event.stopPropagation();
            $('#shoppingBagSvgHoverColor path').attr('fill', '#181D31');
        });
        $('#shoppingBagSvgHoverColor').mouseleave(function(event){
            event.stopPropagation();
            $('#shoppingBagSvgHoverColor path').attr('fill', '#f8f3e5');
        });

        $('#searchBtn').mouseover(function(event){
            event.stopPropagation();
            $('#searchBtn path').attr('fill', '#181D31');
        });
        $('#searchBtn').mouseleave(function(event){
            event.stopPropagation();
            $('#searchBtn path').attr('fill', '#f8f3e5');
        });
    })();
});
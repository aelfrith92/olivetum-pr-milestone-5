/**
* It adds the hovering effect to the shopping bag svg file, which cannot be styled via CSS
*/

$( document ).ready(function() {
    function hoverButtons() {
        
        // Select the path tag inside the svg tag to modify its attribute 'stroke'
        $('#shoppingBag').mouseover(function(event){
            event.stopPropagation();
            $('#shoppingBag path').attr('fill', '#181D31');
        });
        $('#shoppingBag').mouseleave(function(event){
            event.stopPropagation();
            $('#shoppingBag path').attr('fill', '#f8f3e5');
        });

        $('#searchBtn').mouseover(function(event){
            event.stopPropagation();
            $('#searchBtn path').attr('fill', '#181D31');
        });
        $('#searchBtn').mouseleave(function(event){
            event.stopPropagation();
            $('#searchBtn path').attr('fill', '#f8f3e5');
        });
    }
    hoverButtons();
});
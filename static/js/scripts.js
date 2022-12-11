/**
* It adds the hovering effect to the shopping bag svg file, which cannot be styled via CSS
*/

$( document ).ready(function() {
    // Self-invoking f for svg fills
    (function () {
        
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
    })();
    
    // Self-invoking for search input enlarge when focus
    // Script suspended until further optimization
    // (function () {
    //     let textType = false;
    //     let searchInput =  $('#searchContainer input[type="search"]');
    //     let inputWidth = searchInput.width();
    //     console.log(inputWidth);
    //     searchInput.focus(function() {
    //             if (!textType) {
    //                 $(this).animate({
    //                     width: inputWidth*1.5
    //             });
    //         }
    //     });

    //     searchInput.blur(function() {
    //         if(this.value === '') {
    //             $(this).animate({
    //                 width: inputWidth
    //             });
    //         } else {
    //             textType = true;
    //         }
    //     });
    // })();
});
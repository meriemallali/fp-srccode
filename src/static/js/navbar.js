
(function ($) {
    "use strict";
  
    var fullHeight = function() {
  
        $('.js-fullheight').css('height', $(window).height());
        $(window).resize(()=>{
            $('.js-fullheight').css('height', $(window).height());
        });
  
    };
    fullHeight();
   
    $('#sidebarCollapse').on('click',()=> {
      $('#sidebar').toggleClass('active');
      
  });

  
  })(jQuery);
  
$(document).ready(function() {

  $(document).keydown(function(event){

    let key = event.which;

    switch(key) {
      case 39:
        $('#next-page')[0].click();
        break;
      case 37:
        $('#previous-page')[0].click();
        break;
    }
  });

});

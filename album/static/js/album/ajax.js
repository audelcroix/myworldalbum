$(document).ready(function() {

  $('#commentFormEXP').on('submit', function(event){
      event.preventDefault();
      create_post();
  });

  function create_post() {
      let comment_content = $('#commentFormTextarea').val();
      $.ajax({
          url : "/pictures/add_comment/",
          type : "POST",
          data : {
            content : comment_content,
            csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val(),
            photoId: $('#photoId').val()
          },

          success : function(json) {
              $('#commentTextArea').val(''); // remove the value from the input
              if (json.permission) {
                //alert(json.report);
                $("#comment-zone").prepend("<div class='comment-area bg-grey' data-commentId="+json.newCommentId+"> <div class='row no-gutters'> <div class='col-md-2 col-sm-0 profile-pic-area'></div> <div class='col-md-10 col-sm-12 description-area'></div> </div> </div>");
                $("#comment-zone div.profile-pic-area:first").append("<img src='/media/"+json.userImg+"' class='commentProfilePic' alt='"+json.username+"'>");
                $("#comment-zone div.description-area:first").append("<h6 class='pt-1 color-green'>By "+json.username+" <a class='text-danger commentDeleteTrigger float-right mr-2 mt-1'><i class='far fa-trash-alt fa-lg'></i></a></h6><p class='color-white'>"+comment_content+"</p>");

                if ($("#comment-zone").children(".comment-area").length > 5) {
                  $("#comment-zone div.comment-area:last").remove();
                }
                $("#commentFormTextarea").val("");
              } else {
                alert("An error occured");
              }
          },

          error : function(xhr,errmsg,err) {
            $('.error-zone').css("display", "block");
            $('.error-target').val('Sorry, an error occured');
          }
      });
  }

  // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! important
  // ligne pour éliminer le probleme qui empeche le declenchement des scripts apres un machin chargé par ajax
  $('#comment-zone').on('click', '.commentDeleteTrigger', function(event) {
    event.preventDefault();
    let commentId = $(this).closest(".comment-area").attr("data-commentId");
    let targetDiv = $(this).closest(".comment-area");

    $.ajax({
      url: "/pictures/delete_comment/",
      type: "POST",
      data: {
        targetCommentId: commentId,
        photoId: $('#photoId').val(),
        csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()
      },

      success: function(json) {
        //alert(json.permission);
        if (json.permission) {
          targetDiv.remove();
        }
      }
    });

  });


});

$(document).ready(function(){
  $(".default_option").click(function(){
    $(this).parent().toggleClass("active");
  })
  
  $(".default_option label").click(function(){
    $(".default_option").parent().toggleClass("active");
  })

  $(".sortby .select_ul label").click(function(){
    var currentsort = $(this).html();
    $(".sortby .default_option label").html(currentsort);
    $(this).parents(".sortby.select_wrap").removeClass("active");
  })
  // const dropDown = document.querySelector(".sortby.select_wrap");
  // $(".sortby .select_ul label").click(function(){
  //   var currentsort = $(this).html();
  //   $(".sortby .default_option li").html(currentsort);
  //   dropDown.classList.remove("active");
  // })


});

$(function(){
  $('#todo_list').slimScroll({
    position: "right",
    size: "5px",
    height: "315px",
    color: "transparent"
  });

  $('#notifications').slimScroll({
    position: "right",
    size: "5px",
    height: "315px",
    color: "transparent"
  });
});
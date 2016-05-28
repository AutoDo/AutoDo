/**
 * Created by 명 on 2016-05-27.
 */
$(document).ready(function() {
  $(".edit").click(function(event) {
      alert("edit");
    event.preventDefault();
    var intro = $(this).parent("div");
    var content = intro.children("p").first().html().replace(/<br>/g,"\n");
    intro.hide("slow");
    intro.parent('div').append("<form class='intro-form' action='#'>"+
                                      "<div class='mdl-textfield mdl-js-textfield' >"+
                                      "<textarea class='mdl-textfield__input' type='text' rows= '5'>" +
                                        content+
                                      "</textarea>"+
                                      "</div>"+
                                      "<button class='mdl-button mdl-js-button mdl-js-ripple-effect save'>save</button>"+
                                      "</form>");


  });
    
  $('.mdl-card__actions').on("click",".save",function(event) {
      alert("save");
    event.preventDefault();
    var form = $(this).parent("form");
    var intro = form.prev();
    var txt_content =form.find("textarea").first().val().replace(/\n/g, "<br>");
    form.remove();
    intro.children("p").first().html(txt_content);
    intro.show("slow");



  });

  $("body").on("click", ".manage", function(event){

  });

  $("#register").click(function(event){

        $(this).parent("div").addProject({});
  });


  $.fn.addProject = function (data) {


      $(this).append("<div class='mdl-card mdl-shadow--2dp'>"+
                     "<div class='mdl-card__supporting-text'>"+
                     "<h5> Project Name &nbsp; <a>https://github.com</a> </h5>"+
                     "<div class='mdl-grid'>"+
                     "<div class='mdl-cell mdl-cell--6-col'>"+
                     "<label class='mdl-switch mdl-js-switch mdl-js-ripple-effect'>"+
                     "<span class='mdl-switch__label'>Update Periodically</span>"+
                     "<input type='checkbox'  class='mdl-switch__input' checked>"+
                     "</label>"+
                     "</div>"+
                     "<div class='mdl-cell mdl-cell--6-col right'>"+
                     "<button class='mdl-button mdl-js-button mdl-js-ripple-effect refresh'>"+
                     "refresh<i class='material-icons'>autorenew</i>"+
                     "</button>"+
                     "</div>"+
                     "</div>"+
                     "<div class='mdl-grid'>"+
                     "<div class='mdl-cell mdl-cell--6-col'>"+
                     "recent update &nbsp; 2016.05.27"+
                     "</div>"+
                     "<div class='mdl-cell mdl-cell--6-col right'>"+
                     "<button  class='mdl-button mdl-js-button mdl-js-ripple-effect manage'>"+
                     "mange project<i class='material-icons'>build</i>"+
                     "</button>"+
                     "</div>"+
                     "</div>"+
                     "<div class='mdl-grid'>"+
                     "<div class='mdl-cell mdl-cell--12-col label right'>"+
                     "<button class='mdl-button mdl-js-button mdl-js-ripple-effect'>"+
                     "Generate Document NOW"+
                     "</button>"+
                     "</div>"+
                     "</div>"+
                     "</div>"+
                     "<div class='mdl-card__actions mdl-card--border'>"+
                     "<h6>introduction</h6>"+
                     "<p>Project information</p>"+
                     "<button class='mdl-button mdl-js-button mdl-js-ripple-effect edit' >edit</button>"+
                     "</div>"+
                     "</div>"+
                     "</div>");

      componentHandler.upgradeAllRegistered();
  };


});
/**
 * Created by 명 on 2016-05-27.
 */
$(document).ready(function() {
  $("body").on("click",".edit",function(event) {
    event.preventDefault();
    var edit = $(this); 
    var save =edit.next();
    var intro = edit.parent("div").parent("div").parent("div");
    var content = intro.children("p").first().html().replace(/<br>/g,"\n");
    edit.hide();
    save.show();  
    intro.children("p").first().hide("slow");
    intro.append("<form class='intro-form' action='#'>"+
                  "<div class='mdl-textfield mdl-js-textfield' >"+
                  "<textarea class='mdl-textfield__input' type='text' rows= '5'>" +
                    content+
                  "</textarea>"+
                  "</div>"+
                  "</form>");


  });
    
  $('body').on("click",".save",function(event) {
    event.preventDefault();
    var save = $(this);
    var edit = $(this).prev();
    var intro = save.parent("div").parent("div").parent("div");
      
    var form = intro.children("form").first();
    var txt_content =form.find("textarea").first().val().replace(/\n/g, "<br>");
    form.remove();
    intro.children("p").first().html(txt_content).show("slow");
    save.hide();
    edit.show();  




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
                     "<span class='mdl-switch__label'>Update on Every Commit</span>"+
                     "<input type='checkbox'  class='mdl-switch__input' checked>"+
                     "</label>"+
                     "</div>"+
                     "<div class='mdl-cell mdl-cell--6-col right'>"+
                     "<button class='mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect refresh'>"+
                     "Apply Setting<i class='material-icons'>autorenew</i>"+
                     "</button>"+
                     "</div>"+
                     "</div>"+
                     "<div class='mdl-grid'>"+
                     "<div class='mdl-cell mdl-cell--6-col'>"+
                     "recent update &nbsp; 2016.05.27"+
                     "</div>"+
                     "<div class='mdl-cell mdl-cell--6-col right'>"+
                     "<button class='mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect generate'>"+
                     "Generate Document NOW"+
                     "</button>"+
                     "</div>"+
                     "</div>"+
                     "</div>"+
                     "<div class='mdl-card__actions mdl-card--border'>"+
                     "<div class='mdl-grid p0'>"+
                     "<div class='mdl-cell mdl-cell--6-col p0'>"+
                     "<h6>Introduction</h6>"+
                     "</div>"+
                     "<div class='mdl-cell mdl-cell--6-col right p0'>"+
                     "<button class='mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect edit'>edit</button>"+
                     "<button class='mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect save' style='display:none;'>save</button>" +
                     "</div>"+
                     "</div>"+
                     "<p>{{ item.project_desc }}</p>"+
                      "</div>"+
                      "</div>"+
                     "</div>");

      componentHandler.upgradeAllRegistered();
  };


});
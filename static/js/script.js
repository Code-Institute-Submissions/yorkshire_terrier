// for mobile navbar
$(document).ready(function(){
    $('.sidenav').sidenav();
// for adding your dog 
    $('.collapsible').collapsible();
// to see if which dogs have found their match
    $(".tooltipped").tooltip();
// to initialize scripts
    $('select').formSelect();
// delete confirmation modal 
    $('.modal').modal(); 
 });


 
// to validate cities drop down to make sure its do validate and makes sure you have chosen one option
// Thanks for code snipet to Code Institute walk thru video
$(document).ready(function(){
     validateMaterializeSelect();
    function validateMaterializeSelect() {
        let classValid = { "border-bottom": "1px solid #4caf50", "box-shadow": "0 1px 0 0 #4caf50" };
        let classInvalid = { "border-bottom": "1px solid #f44336", "box-shadow": "0 1px 0 0 #f44336" };
        if ($("select.validate").prop("required")) {
            $("select.validate").css({ "display": "block", "height": "0", "padding": "0", "width": "0", "position": "absolute" });
        }
        $(".select-wrapper input.select-dropdown").on("focusin", function () {
            $(this).parent(".select-wrapper").on("change", function () {
                if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () { })) {
                    $(this).children("input").css(classValid);
                }
            });
        }).on("click", function () {
            if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
                $(this).parent(".select-wrapper").children("input").css(classValid);
            } else {
                $(".select-wrapper input.select-dropdown").on("focusout", function () {
                    if ($(this).parent(".select-wrapper").children("select").prop("required")) {
                        if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
                            $(this).parent(".select-wrapper").children("input").css(classInvalid);
                        }
                    }
                });
            }
        });
    }
  });

// for automatic year update for copyrights
   $("#copyright").text(new Date().getFullYear());


// avatar pic for reviews animation
$("img.avatarpic").mouseenter(function(){
    $(this).animate({
      opacity: "1",
      height: "150px",
      width: "150px"
    });
  });
$("img.avatarpic").mouseleave(function(){
    $(this).animate({
      opacity: "1",
      height: "100px",
      width: "100px"
    });
  });

// for paragraph hover changing color
$(".hover").mouseenter(function(){
$(this).css("color", "darkGreen");
});
$(".hover").mouseleave(function(){
$(this).css("color", "black");
});
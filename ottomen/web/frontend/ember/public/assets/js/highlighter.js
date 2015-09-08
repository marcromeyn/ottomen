(function ($) {
    $.fn.highlighter = function (options) {
        var settings = $.extend({
            // Defaults.
            highlighted: "highlighter"
        }, options);
        var getSelText = function (target) {
            var sel = window.getSelection ? window.getSelection() : document.selection.createRange(); // FF : IE
            if (sel.getRangeAt) { // thats for FF
                var range = sel.getRangeAt(0);
                var contents = $(range.cloneContents());
                var newNode = document.createElement("span");
                newNode.setAttribute('class', 'highlighter');
                if(contents.children('.highlighter').size() == 0){
                  range.surroundContents(newNode);
                }else{
                  var text = range.toString();
                  range.deleteContents();
                  newNode.appendChild(document.createTextNode(text))
                  range.insertNode(newNode);
                  $('span.highlighter:empty').remove()
                }

            } else { //and thats for IE7
                sel.pasteHTML('<span class="highlighter">' + sel.htmlText + '</span>');
            }
        }

        return this.each(function () {
            var flag = 0,
                element = this;
            element.addEventListener("mousedown", function () {
                flag = 0;
            }, false);
            element.addEventListener("mousemove", function () {
                flag = 1;
            }, false);
            element.addEventListener("mouseup", function (e) {
                if (flag === 0) {
                    console.log("click");
                } else if (flag === 1) {
                    var target = $(e.target);
                    if(!target.hasClass("highlighter")){
                        getSelText();
                    }else{
                      window.getSelection().removeAllRanges();
                    }
                }
            }, false);
            element.addEventListener("dblclick", function (e) {
              var target = $(e.target);
              if(!target.hasClass("highlighter")){
                  getSelText();
              }else{
                window.getSelection().removeAllRanges();
              }
            }, false);
        });
    };
}(jQuery));

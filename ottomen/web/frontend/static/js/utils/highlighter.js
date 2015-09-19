var $ = require('jquery');

window.removeHighlightText = function(elem){
    $(elem).contents().unwrap();
    $('#text')[0].normalize();
}
module.exports = function (id) {

    var getSelText = function (target) {
        var sel = window.getSelection ? window.getSelection() : document.selection.createRange(); // FF : IE
        if (sel.getRangeAt) { // thats for FF
            var range = sel.getRangeAt(0);
            var contents = $(range.cloneContents());
            var span = document.createElement("span");
            span.setAttribute('onclick', 'window.removeHighlightText(this)');
            span.setAttribute('class', 'highlighter');
            if(contents.children('.highlighter').size() == 0){
              window.mytest = {span: span, range: range, contents: contents};
              range.surroundContents(span);
            }else{
              var text = range.toString();
              range.deleteContents();
              span.appendChild(document.createTextNode(text))
              range.insertNode(span);
              $('span.highlighter:empty').remove()
            }

        } else { //and thats for IE7
            sel.pasteHTML('<span class="highlighter">' + sel.htmlText + '</span>');
        }
    }

    return $(id).each(function () {
        var flag = 0,
            element = this;
        element.addEventListener("mousedown", function () {
            flag = 0;
        }, false);
        element.addEventListener("mousemove", function () {
            flag = 1;
        }, false);
        element.addEventListener("mouseup", function (e) {
            if (flag === 1) {
                var target = $(e.target);
                if(!target.hasClass("highlighter")){
                    getSelText();
                }
                window.getSelection().removeAllRanges();
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

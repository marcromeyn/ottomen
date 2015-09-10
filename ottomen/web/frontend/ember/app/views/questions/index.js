import Ember from 'ember';

export default Ember.View.extend({
  actions:{
    next: function(){
      var questions_type = this.get('controller').model.get('questions_type');
      if(questions_type == "string"){
        var answers = $('.highlighter').map(function(){return $(this).text();});
        $('.highlighter').map(function(){return $(this).contents().unwrap();});
        $('#text')[0].normalize();
        this.get("controller").send("next", answers);
      }
      if(questions_type == "boolean"){
        var answers = $('input[name=answer]:checked').val();
        if(answers){
          $('#instructions').removeClass('error')
          $('input[name=answer]:checked').prop('checked', false);
          this.get("controller").send("next", answers);
        }else{
          $('#instructions').addClass('error')
        }
      }

    }
  },
  selectText: function(){
    var text = "";
    if (window.getSelection) {
        text = window.getSelection().toString();
    } else if (document.selection && document.selection.type !== "Control") {
        text = document.selection.createRange().text;
    }
    return text;
  },
  highlightText: function(){
    var range = window.getSelection().getRangeAt(0);
    var selectionContents = range.extractContents();
    var span = document.createElement("span");
    span.appendChild(selectionContents);
    span.setAttribute("class", "uiWebviewHighlight selectedText");
    span.setAttribute('onclick', 'highlightText(this)');
    span.style.backgroundColor = "red";
    span.style.color = "white";

    range.insertNode(span);
  }
  // eventManager: Ember.Object.create({
  //   mouseUp: function(event, view) {
  //     var text = view.selectText();
  //     var selection = window.getSelection();
  //     // if(text && (selection.anchorNode.data.replace('\n', '') === question.innerText.replace('\n', ''))){
  //       view.highlightText();
  //       $('#text')[0].normalize();
  //     // }
  //     window.getSelection().removeAllRanges();
  //   }
  // })
});

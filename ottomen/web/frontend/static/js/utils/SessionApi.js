var Promise = require('promise');

module.exports = {

  // Load mock product data from localStorage into ProductStore via Action
  createSession: function(assignmentId, workerId) {
    return  new Promise(function (resolve, reject) {
      var data = JSON.parse(localStorage.getItem('session'));
      if(data){
        resolve(data);
      }else{
        reject("Shit went wrong");
      }
    });
  }

};

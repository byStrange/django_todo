function addTodo(todoListSlug, $) {
  var title =  document.querySelector('.form-outline #title').value;
  var data = {
    todo_list_slug: todoListSlug,
    title: title,
    memo: "",
    important: false,
    done: false,
    starred: false,
    dateCompleted: null,
    dateCreated: new Date(),
    csrfmiddlewaretoken: document.querySelector('input[name="csrfmiddlewaretoken"]').value
  };
  // with XMLHttpRequest
  var xhr = new XMLHttpRequest(); // or Microsoft.AcitveObject("Msxml2.XMLHTTP")
  xhr.open("POST", "/todo/add/", true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(JSON.stringify(data));
  xhr.onreadystatechange = function () {
    if (xhr.readyState == 4) {
      if (xhr.status == 200) {
        alert("Sucessfully sent");
      } else {
        alert("Error: " + xhr.status);
      }
    } else {
      alert("Error: " + xhr.status);
    }
  };
}

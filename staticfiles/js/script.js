function addTodo(todoListSlug) {
  var title = document.querySelector('.form-outline #title').value;
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
  // var xhr = new XMLHttpRequest(); // or Microsoft.AcitveObject("Msxml2.XMLHTTP")
  // xhr.setRequestHeader("Content-Type", "application/json");
  var json_data = JSON.stringify(data)
  // xhr.open("GET", "/todo/add/" + json_data, true);
  // xhr.send();
  if (window.XMLHttpRequest) {
    var xhttp = new XMLHttpRequest();
  } else { // code for IE6, IE5
    var xhttp = new ActiveXObject("Microsoft.XMLHTTP");
  }
  xhttp.onreadystatechange = function () {
    if (xhttp.readyState === 4 && xhttp.status === 200) {
      var data = JSON.parse(this.responseText);
      console.log(data)
      var wrapper = document.querySelector('#todo_wrapper');
      if (data.status == 200) {
        var element = document.createElement('div'); element.className = "col-12  "
        element.innerHTML = `
        <div class="todo todo-primary">
          <div class="d-flex gap-2">
            <div class="todo-action is-done">
              <input
                type="checkbox"
                class="todo-check form-check-input"
                id="${data.id}"
              />
            </div>
            <div class="todo-title">${data.title}</div>
          </div>
          <div class="todo-actions">
            <button
              class="todo-action todo-action-edit"
              style="--delay: 100ms; --color: black"
            >
              <i class="fas fa-pencil-alt"></i>
            </button>
            <button
              class="todo-action todo-action-delete"
              style="--delay: 50ms; --color: red"
            >
              <i class="fas fa-trash-alt"></i>
            </button>
          </div>
        </div>
        `
        wrapper.appendChild(element);
      }
    } else {
      console.log('Not yet')
    }
  }
  var url = "/todo/add/"
  xhttp.open("GET", url + `?data=${json_data}`, true);
  xhttp.send();
}
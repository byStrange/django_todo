Object.prototype.stringify = function () {
  return JSON.stringify(this);
};

String.prototype.parse = function () {
  return JSON.parse("" + this); //?  this = object so we converted it to string
};

var url = "/todo/change/"; // this url for both adding and editing )

function addTodo(todoListSlug) {
  var title = document.querySelector(".form-outline #title");
  var data = {
    action: "C", //?  "C" stands for "CREATE" at CRUD
    todo_list_slug: todoListSlug,
    title: title.value,
    memo: "",
    important: false,
    done: false,
    starred: false,
    dateCompleted: null,
    dateCreated: new Date(),
    csrfmiddlewaretoken: document.querySelector(
      'input[name="csrfmiddlewaretoken"]'
    ).value,
  }.stringify();
  var xhttp = window.XMLHttpRequest
    ? new window.XMLHttpRequest()
    : new ActiveXObject("Microsoft.XMLHTTP");
  xhttp.onreadystatechange = function () {
    if (xhttp.readyState === 4 && xhttp.status === 200) {
      var data = JSON.parse(this.responseText);
      var unDoneTodosContainer = document.querySelector(".todos.todos-undone");
      if (data.ok) {
        title.value = "";
        var element = document.createElement("div");
        element.className = "col-12";
        element.innerHTML = `
        <div class="todo shadow-sm border todo-primary" id="todo${data.id}">
          <div class="d-flex gap-2">
            <div class="todo-action is-done">
              <input
                type="checkbox"
                class="todo-check form-check-input"
                id="${data.id}"
                data-ref="trigger"
              />
            </div>
            <div class="todo-title">${data.title}</div>
          </div>
          <div class="todo-actions">
          <button
            class="todo-action todo-action-star"
            style="--delay: 150ms; --color: red"
          >
            <i class="fas fa-heart"></i>
          </button>
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
        `;
        unDoneTodosContainer.appendChild(element);
        reload(document);
      }
    } else {
      console.log("Error adding data");
    }
  };
  xhttp.open("GET", url + `?data=${data}`, true);
  xhttp.send();
}

var reload = function ($) {
  $.querySelectorAll('[data-ref="trigger"]') // trigger for mark todo as done
    .forEach((trigger) => {
      var todoId = trigger.id || trigger.getAttribute("id");
      trigger.onchange = function () {
        var _do = this.checked ? "mark" : "unmark";
        var data = {
          id: todoId,
          action: "E",
          do: _do,
        }.stringify();
        var http = window.XMLHttpRequest
          ? new window.XMLHttpRequest()
          : new ActiveXObject("Microsoft.XMLHTTP");
        http.onreadystatechange = function () {
          if (http.readyState == 4 && http.status == 200) {
            var response = this.responseText.parse();
            if (response.ok) {
              var { response } = response;
              console.log(response.id);
              var doneTodosContainer = $.querySelector(".todos.todos-done");
              var unDoneTodosContainer = $.querySelector(".todos.todos-undone");
              var todo = document.querySelector(`#todo${response.id}`);
              var todoTitle = todo.querySelector(".todo-title");
              if (response.done) {
                todoTitle.className = "todo-title text-muted";
                todo.className = "todo todo-done";
                todo = todo.parentElement;
                doneTodosContainer.appendChild(todo);
              } else {
                todoTitle.classList.remove("text-muted");
                todo.className = "todo shadow-sm border todo-primary";
                todo = todo.parentElement;
                unDoneTodosContainer.appendChild(todo);
              }
            }
          }
        };
        http.open("GET", url + `?data=${data}`, true);
        http.send();
      };
    });
};

reload(document);

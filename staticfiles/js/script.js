Object.prototype.stringify = function () {
  return JSON.stringify(this);
};

String.prototype.parse = function () {
  return JSON.parse("" + this); //?  this = object so we converted it to string
};

const customAlert = {
  duration: 2000,
};
var url = "/todo/change/"; // this url for both adding and editing )

const addTodo = function (todoListSlug) {
  var title = document.querySelector(".form-outline #title");
  var data = {
    action: "C", //?  "C" stands for "CREATE" at CRUD
    todo_list_slug: todoListSlug,
    title: title.value,
    memo: "",
    important: false,
    done: false,
    do: "create_todo",
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
  if (title.value) {
    xhttp.open("GET", url + `?data=${data}`, true);
    xhttp.send();
  } else {
    _alert({
      title: "Error",
      text: "task name is required",
      type: "danger",
      duration: 2000,
    });
  }
};

const reload = function ($) {
  $.querySelectorAll('[data-ref="trigger"]') // trigger for mark todo as done
    .forEach((trigger) => {
      var todoId = trigger.id || trigger.getAttribute("id");
      trigger.onchange = function () {
        var _do = this.checked ? "mark" : "unmark";
        var data = {
          id: todoId,
          action: "U", //? "U" stands for "UPDATE" at CRUD
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

var modal = {
  self: document.querySelector(".modal"),
  openers: document.querySelectorAll("#openModal, .open-modal"),
  closers: document.querySelectorAll("#closeModal, .close-modal"),
  show: function () {
    showModal(this);
  },
  hide: function () {
    hideModal(this);
  },
};

modal.openers.forEach((opener) => {
  opener.onclick = (e) => modal.show();
});

modal.closers.forEach((closer) => {
  closer.onclick = (e) => modal.hide();
});

function showModal({ self }) {
  self.classList.add("show");
  self.classList.remove("hide");
}

function hideModal({ self }) {
  self.classList.remove("show");
  self.classList.add("hide");
}

const createList = function () {
  var title = document.querySelector(".modal #title");
  var memo = document.querySelector(".modal #memo");
  var data = {
    action: "C", //? "C" stands for "CREATE" at CRUD
    title: title.value,
    memo: memo.value,
    slug: title.value.toLowerCase().replace(/\s/g, "-"),
    do: "create_list",
  }.stringify();
  var xhttp = window.XMLHttpRequest
    ? new window.XMLHttpRequest()
    : new ActiveXObject("Microsoft.XMLHTTP");
  xhttp.onreadystatechange = function () {
    if (xhttp.readyState === 4 && xhttp.status === 200) {
      var data = JSON.parse(this.responseText);
      var { response } = data;
      console.log(response);
      if (response.ok) {
        modal.hide();
      }
    } else {
      console.log("Error adding data" + this.responseText);
    }
  };

  if (title.value.length > 0) {
    console.log("Sending data: " + data);
    xhttp.open("GET", url + `?data=${data}`, true);
    xhttp.send();
  } else {
    console.log("Title is empty");
    var alertOpts = {
      text: "Title name is required",
      duration: 2500,
      type: "warning",
      callback() {
        console.log("alert closed");
      },
    };
    _alert(alertOpts);
  }
};

function _alert({ text, duration, type, callback }) {
  const dur = duration || 2000; //? default duration is 2 seconds
  var alert = document.createElement("div");
  const aleryStyles = {
    transition: "all 0.5s ease-in-out",
    position: "fixed",
    right: -200 + "%",
    top: 10 + "px",
    padding: 10 + "px",
    borderRadius: 5 + "px",
    zIndex: 9999,
    textAlign: "center",
  }; //? default styles
  Object.assign(alert.style, aleryStyles);
  document.body.appendChild(alert);
  alert.style.right = 0;
  alert.className = "alert border shadow alert-" + type;
  alert.innerHTML = text;
  Object.assign(alert.style);
  setTimeout(() => {
    var x = +alert.offsetWidth * 2;
    alert.style.right = -x + "px";
    alert.style.opacity = 0;
    setTimeout(() => {
      alert.remove();
      if (callback) callback();
    }, 500);
  }, dur);
} //? _alert is a private function

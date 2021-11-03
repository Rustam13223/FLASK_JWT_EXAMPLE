function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

async function addTask() {
  const text = document.getElementById('task_field').value
  const options = {
    method: 'post',
    credentials: 'same-origin',
    headers: {
      'X-CSRF-TOKEN': getCookie('csrf_access_token'),
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({"task": text})
  };
  fetch('/tasks/add', options).then((_res) => {
    window.location.href = "/tasks";
  });
}

async function deleteTask(_id) {
  const options = {
    method: 'post',
    credentials: 'same-origin',
    headers: {
      'X-CSRF-TOKEN': getCookie('csrf_access_token'),
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({"_id": _id})
  };
  fetch('/tasks/delete', options).then((_res) => {
    window.location.href = "/tasks";
  });
}

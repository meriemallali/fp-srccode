const id = JSON.parse(document.getElementById("user-id").textContent);
const message_owner = JSON.parse(
  document.getElementById("user-id").textContent
);
const receiver = JSON.parse(document.getElementById("receiver-id").textContent);
const currentuser_username = JSON.parse(
  document.getElementById("user-username").textContent
);
wsURL = `ws://${window.location.host}/ws/${id}`;

const websocket = new WebSocket(wsURL);

websocket.onopen = (event) => {
  console.log("Accepted Connection", event);
};

websocket.onclose = (event) => {
  console.log("Lost Connection", event);
};

websocket.onerror = (event) => {
  console.log("Error Occured while connecting:", event);
};

websocket.onmessage = function (event) {
  const message_data = JSON.parse(event.data);
  if (message_data.username === currentuser_username) {
    document.querySelector("#message").innerHTML += `
      <div class="d-flex flex-row justify-content-end mb-4 pt-1">
        <div>
          <p class="small p-2 me-3 mb-1 text-white rounded-3" style="background-color:#5457a1">${message_data.message}</p>
          <p class="small me-3 mb-3 rounded-3 text-muted d-flex justify-content-end">just now</p>
        </div>
      </div>`;
  } else {
    document.querySelector("#message").innerHTML += `    
      <div class="d-flex flex-row justify-content-start">
        <div>
          <p class="small p-2 ms-3 mb-1 rounded-3" style="background-color:#f5f6f7;">${message_data.message}</p>
          <p class="small ms-3 mb-3 rounded-3 text-muted">just now</p>
        </div>                  
      </div>`;
  }
};

document.querySelector("#message-submit").onclick = function (event) {
  const input = document.querySelector("#input");
  const message = input.value;

  websocket.send(
    JSON.stringify({
      message: message,
      sent_by: message_owner,
      sent_to: receiver,
    })
  );

  event.preventDefault();
  input.value = "";
};


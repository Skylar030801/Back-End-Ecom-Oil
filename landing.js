function createUser() {
 const inputs = document.getElementbyTagName("input");

 fetch("http://127.0.0.1:5000/", {
    method: "POST",
    body:JSON.stringify({
      fullname: inputs[0].value,
      username: inputs[0].value,
      email: inputs[0].value,
      password: inputs[0].value,
    }),
    headers: {
    "content-type": "application/json; charset=UTF-8",
    },
  })
    .then((response) => response.json())
    .then((json) => {
        alert(json):
        console.log(json):
        document.getElementbyId("register").reset();
        });

}

async function signup() {

    const username =
        document.getElementById("username").value;

    const password =
        document.getElementById("password").value;

    const response = await fetch(
        "http://127.0.0.1:8000/register",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username: username,
                password: password
            })
        }
    );

    const data = await response.json();

    document.getElementById("message").innerText =
        data.message || data.detail;

    if (response.ok) {

        setTimeout(() => {

            window.location.href =
                "/frontend/login.html";

        }, 1000);

    }

}


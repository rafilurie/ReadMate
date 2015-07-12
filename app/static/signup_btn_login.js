window.onload = function() {
    
    var clickedBtn = 2;

    document.getElementById("signup-btn").onclick = function() {
        clickedBtn = 1;
        window.location.href='/welcome';
    }

    document.getElementById("login-btn").onclick = function() {
        clickedBtn = 2;
        window.location.href='/welcome/login';
    }

    document.getElementById("signup-btn").onmouseover = function() {
        this.style.backgroundColor = "#F6C991";
        this.style.color = "white";
        document.getElementById("login-btn").style.backgroundColor = "white";
        document.getElementById("login-btn").style.color = "#F6C991";
    }

    document.getElementById("login-btn").onmouseover = function() {
        this.style.backgroundColor = "#F6C991";
        this.style.color = "white";
        document.getElementById("signup-btn").style.backgroundColor = "white";
        document.getElementById("signup-btn").style.color = "#F6C991";
    }

    document.getElementById("signup-btn").onmouseout = function() {
        if (clickedBtn == 1) {
            this.style.backgroundColor = "#F6C991";
            this.style.color = "white";
            document.getElementById("login-btn").style.backgroundColor = "white";
            document.getElementById("login-btn").style.color = "#F6C991";
        } else {
            this.style.backgroundColor = "white";
            this.style.color = "#F6C991";
            document.getElementById("login-btn").style.backgroundColor = "#F6C991";
            document.getElementById("login-btn").style.color = "white";
        }
    }

    document.getElementById("login-btn").onmouseout = function() {
        if (clickedBtn == 2) {
            this.style.backgroundColor = "#F6C991";
            this.style.color = "white";
            document.getElementById("signup-btn").style.backgroundColor = "white";
            document.getElementById("signup-btn").style.color = "#F6C991";
        } else {
            this.style.backgroundColor = "white";
            this.style.color = "#F6C991";
            document.getElementById("signup-btn").style.backgroundColor = "#F6C991";
            document.getElementById("signup-btn").style.color = "white";
        }
    }
}
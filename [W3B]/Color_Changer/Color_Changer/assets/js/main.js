let btns = document.getElementsByClassName("btn");

for (let i=0; i < btns.length; i++) {
    btns[i].addEventListener("click", function(){
        let buttonStyle = getComputedStyle(this);
        let buttonBgColor = buttonStyle["backgroundColor"];

        if (String(buttonBgColor) == "rgba(128, 37, 198, 0.8)") {
            let token = ("../assets/css/main.css")
            
            document.getElementById('trainpic').classList.remove('red');
            document.getElementById('trainpic').classList.remove('green');
            document.getElementById('trainpic').classList.add('purple');

        }
        else if (String(buttonBgColor) == "rgba(0, 128, 0, 0.8)"){
            document.getElementById('trainpic').classList.remove('purple');
            document.getElementById('trainpic').classList.remove('red');
            document.getElementById('trainpic').classList.add('green');
        }
        else {
            document.getElementById('trainpic').classList.remove('green');
            document.getElementById('trainpic').classList.remove('purple');
            document.getElementById('trainpic').classList.add('red');
        }
        
    });
}
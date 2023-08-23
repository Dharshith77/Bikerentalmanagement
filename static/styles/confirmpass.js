let pass1 = document.getElementById('password');
let pass2 = document.getElementById('confirmpass');
let message =document.getElementById('message');
function check_password() {
    if (pass1.value === pass2.value) {
        message.textContent = 'Matched';
        message.style.color = 'green'; // Set text color to green for matching
    } else {
        message.textContent = 'Not Matched';
        message.style.color = 'red'; // Set text color to red for not matching
    }
}
pass1.addEventListener('keyup',()=>{
if(pass2.value.length!=0) check_password();
}
)
pass2.addEventListener('keyup',check_password);



function validation_register(){
    if

}


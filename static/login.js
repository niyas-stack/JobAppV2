function validate() {
 var email = document.forms["myForm"]["email"].value.trim();
 var password = document.forms["myForm"]["password"].value.trim();
 if(email==""){
 alert("Email must be filled");
 return false;
 }
 else{
 let regEmail = /^[a-zA-Z0-9]+@+[A-Za-z]+\.[A-Za-z]{3}$/;
 let result3 = regEmail.test(email);
 if(!result3){
 alert("Invalid mail id.")
 return false;
 }}
 if(password==""){
 alert("Password must be filled");
 return false;
 }
 else if (password.length<6){
 alert("Password length must be grater than or equal to 6");
 return false;
 }
 }
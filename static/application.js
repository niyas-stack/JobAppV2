function validateForm()
{
 let a = document.forms["myForm"]["name"].value;
 var regName = /^[A-Za-z][A-Za-z\s]*$/;
 if (a == ""||a==null)
 {
 alert("Name cannot be blank");
 return false;
 }
 if(!regName.test(a))
 {
 alert("Enter name using Alphabets only");
 return false;
 }

 let b = document.forms["myForm"]["email"].value;
 let regEmail = /^[A-Za-z0-9.]+@+[a-z]+\.[a-z]{3}$/;
 if(b == "")
 {
 alert("Email must be filled out");
 return false;
 }
 if(!regEmail.test(b))
 {
 alert("Invalid Email format");
 return false;
 }
 }
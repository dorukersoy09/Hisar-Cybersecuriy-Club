// Front-end only demo. There is no real authentication here:
// GitHub Pages serves static files, so it cannot check passwords securely.
// To make it real, send the form data to a backend (your own server,
// Firebase Auth, Supabase, etc.) instead of the fake flow below.
 
const signinScreen = document.getElementById("screen-signin");
const passwordScreen = document.getElementById("screen-password");
 
const signinForm = document.getElementById("signin-form");
const identifier = document.getElementById("identifier");
const identifierError = document.getElementById("identifier-error");
const identifierDisplay = document.getElementById("identifier-display");
 
const passwordForm = document.getElementById("password-form");
const password = document.getElementById("password");
const passwordError = document.getElementById("password-error");
const changeLink = document.getElementById("change-identifier");
const message = document.getElementById("form-message");
 
function showScreen(screen) {
  signinScreen.classList.add("hidden");
  passwordScreen.classList.add("hidden");
  screen.classList.remove("hidden");
}
 
// --- Page 1: identifier -> continue ---
signinForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const value = identifier.value.trim();
 
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const phonePattern = /^[+]?[\d\s()-]{7,}$/;
 
  if (!value) {
    identifierError.textContent = "Enter your mobile number or email.";
    identifier.classList.add("invalid");
    return;
  }
  if (!emailPattern.test(value) && !phonePattern.test(value)) {
    identifierError.textContent = "Enter a valid email or phone number.";
    identifier.classList.add("invalid");
    return;
  }
 
  identifierError.textContent = "";
  identifier.classList.remove("invalid");
  identifierDisplay.textContent = value;
  showScreen(passwordScreen);
});
 
// --- Change identifier -> back to Page 1 ---
changeLink.addEventListener("click", (e) => {
  e.preventDefault();
  message.textContent = "";
  message.className = "message";
  showScreen(signinScreen);
});
 
// --- Page 2: password -> sign in ---
passwordForm.addEventListener("submit", (e) => {
  e.preventDefault();
  message.textContent = "";
  message.className = "message";
 
  if (!password.value) {
    passwordError.textContent = "Enter your password.";
    password.classList.add("invalid");
    return;
  }
  if (password.value.length < 6) {
    passwordError.textContent = "Your password is incorrect.";
    password.classList.add("invalid");
    return;
  }
 
  passwordError.textContent = "";
  password.classList.remove("invalid");
 
  // Simulated request. Replace with a real fetch() to your backend.
  message.textContent = "Demo only: form is valid, but no account system is connected.";
  password.value = "";
});
 

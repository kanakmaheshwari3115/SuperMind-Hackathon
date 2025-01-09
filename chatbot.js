
const chatbot = document.getElementById('chatbot');
const conversation = document.getElementById('conversation');
const inputForm = document.getElementById('input-form');
const inputField = document.getElementById('input-field');
inputForm.addEventListener('submit', function(event) {
  
  event.preventDefault();

 
  const input = inputField.value;

 
  inputField.value = '';
  const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: "2-digit" });

  let message = document.createElement('div');
  message.classList.add('chatbot-message', 'user-message');
  message.innerHTML = `<p class="chatbot-text" sentTime="${currentTime}">${input}</p>`;
  conversation.appendChild(message);

 
  const response = generateResponse(input);

 
  message = document.createElement('div');
  message.classList.add('chatbot-message','chatbot');
  message.innerHTML = `<p class="chatbot-text" sentTime="${currentTime}">${response}</p>`;
  conversation.appendChild(message);
  message.scrollIntoView({behavior: "smooth"});
});


function generateResponse(input) {
   
    const responses = [
      "Hi there! How can I make your day better today? 😊",
      "I'm sorry, could you clarify your question? I'd love to help! 😕",
      "Here to assist! Feel free to ask me anything you need. 📩",
      "I currently can't access the internet, but let's see what I can do to assist you! 💻",
      "What sparks your curiosity today? 🤔",
      "Let's keep our conversation respectful and positive. 🚫",
      "I'm excited to help you out! What's on your mind? 🚀",
      "Anything specific you'd like to dive into? 💬",
      "I'm all ears! Let me know how I can support you. 😊",
      "How can I make things easier for you today? 🤗",
      "Have any specific questions or topics in mind? I'm ready to assist! 💡",
      "Let's tackle your queries together! What would you like to discuss? 💬",
    
    ];
    
    
    return responses[Math.floor(Math.random() * responses.length)];
  }
  

  window.onblur = function (tabs) { 
alert('trying to switch tabs eh !'); 
  };
  
  
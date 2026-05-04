document.addEventListener('DOMContentLoaded', () => {

  const form = document.getElementById('chat-form');
  const textarea = document.getElementById('mensaje-input');

  const chatArea = document.querySelector('.chat-area');
  if (chatArea) {
    chatArea.scrollTop = chatArea.scrollHeight;
  }

  if (textarea && form) {
    textarea.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        if (textarea.value.trim()) form.submit();
      }
    });
    textarea.focus();
  }

  document.querySelectorAll('.option-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      btn.classList.toggle('active');
    });
  });

  document.querySelectorAll('.suggestion-card').forEach(card => {
    card.addEventListener('click', () => {
      const title = card.querySelector('.card-title').textContent;
      if (textarea) {
        textarea.value = 'Quiero ' + title.toLowerCase() + ': ';
        textarea.focus();
      }
    });
  });

});

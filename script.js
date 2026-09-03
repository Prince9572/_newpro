// Theme toggle with persistence
const root = document.documentElement;
const toggleBtn = document.getElementById('themeToggle');

function applyTheme(theme){
  if(theme === 'light'){
    root.setAttribute('data-theme', 'light');
  } else {
    root.removeAttribute('data-theme');
  }
}

const saved = localStorage.getItem('theme');
if(saved){
  applyTheme(saved);
} else {
  // default to dark; respect OS light preference only if explicitly light
  const prefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
  applyTheme(prefersLight ? 'light' : 'dark');
}

toggleBtn.addEventListener('click', () => {
  const isLight = root.getAttribute('data-theme') === 'light';
  const next = isLight ? 'dark' : 'light';
  applyTheme(next);
  localStorage.setItem('theme', next);
});

// Terminal typing effect for "whoami"
const whoamiOut = document.getElementById('whoamiOut');
const whoamiText = 'Prince Kumar — Full-Stack Developer & AI Agent Developer';
let i = 0;

function typeWhoami(){
  if(i <= whoamiText.length){
    whoamiOut.textContent = whoamiText.slice(0, i);
    i++;
    setTimeout(typeWhoami, 28);
  }
}
typeWhoami();

// Footer year
document.getElementById('year').textContent = new Date().getFullYear();

(()=>{'use strict';function init(hero){const video=hero.querySelector('[data-hero-video]'),button=hero.querySelector('[data-motion-toggle]');if(!video||!button||video.dataset.ready)return;video.dataset.ready='true';const reduced=window.matchMedia('(prefers-reduced-motion: reduce)'),mobile=window.matchMedia('(max-width: 760px)');let userPaused=false,inView=true,userRequested=false;
const sync=()=>{const playing=!video.paused&&!video.ended;button.querySelector('[data-motion-label]').textContent=playing?'PAUSE FILM':'PLAY FILM';button.querySelector('[data-motion-icon]').textContent=playing?'Ⅱ':'▶';button.setAttribute('aria-label',playing?'Pause campaign video':'Play campaign video')};
function source(){if(!video.getAttribute('src')){video.src=mobile.matches?video.dataset.mobile:video.dataset.desktop;video.muted=true;video.defaultMuted=true;video.load()}}
async function play(explicit=false){if(!explicit&&(reduced.matches||navigator.connection?.saveData||userPaused||document.hidden||!inView))return;source();try{await video.play()}catch{sync()}}
button.hidden=false;button.addEventListener('click',()=>{if(!video.paused){userPaused=true;userRequested=false;video.pause()}else{userPaused=false;userRequested=true;play(true)}});
video.addEventListener('playing',()=>{video.classList.add('is-playing');sync()});video.addEventListener('pause',sync);video.addEventListener('error',()=>{video.classList.remove('is-playing');button.hidden=true});
reduced.addEventListener('change',()=>{if(reduced.matches){userRequested=false;video.pause();video.classList.remove('is-playing')}else play()});
document.addEventListener('visibilitychange',()=>{if(document.hidden)video.pause();else if(userRequested&&!userPaused&&inView)play(true);else play()});
if('IntersectionObserver' in window){const observer=new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;if(inView){if(userRequested&&!userPaused)play(true);else play()}else video.pause()},{threshold:0.1});observer.observe(hero)}
play();sync();}
document.querySelectorAll('.hero').forEach(init);document.addEventListener('shopify:section:load',e=>{const hero=e.target.querySelector('.hero');if(hero)init(hero)});
})();

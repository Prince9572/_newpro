// MUSIC

const music =
document.getElementById("bgMusic")

const musicBtn =
document.getElementById("musicBtn")

let userPausedMusic = false
let resumeMusicTimeout

function updateMusicButton(){

  const label =
  music.paused ?
  "Play music" :
  "Pause music"

  musicBtn.setAttribute(
  "aria-label",
  label)

  musicBtn.setAttribute(
  "title",
  label)

  musicBtn.classList.toggle(
  "is-playing",
  !music.paused)

}

async function playMusic(){

  if(userPausedMusic){
    return
  }

  try{

    await music.play()

  }catch(error){

    updateMusicButton()

  }

}

function resumeMusicSoon(){

  if(userPausedMusic || music.ended){
    return
  }

  clearTimeout(resumeMusicTimeout)

  resumeMusicTimeout =
  setTimeout(()=>{
    playMusic()
  },250)

}

musicBtn.onclick = async ()=>{

  if(music.paused){

    userPausedMusic = false
    await playMusic()

  }else{

    userPausedMusic = true
    music.pause()

  }

  updateMusicButton()

}

music.addEventListener(
"play",
updateMusicButton)

music.addEventListener(
"pause",
()=>{

  updateMusicButton()

  if(
    !userPausedMusic &&
    !music.ended &&
    document.visibilityState ===
    "visible"
  ){

    resumeMusicSoon()

  }

})

music.addEventListener(
"ended",
()=>{

  if(userPausedMusic){
    return
  }

  music.currentTime = 0
  playMusic()

})

music.addEventListener(
"stalled",
resumeMusicSoon)

music.addEventListener(
"suspend",
resumeMusicSoon)

document.addEventListener(
"visibilitychange",
()=>{

  if(
    document.visibilityState ===
    "visible"
  ){

    playMusic()

  }

})

window.addEventListener(
"focus",
playMusic)

window.addEventListener(
"pageshow",
playMusic)

window.addEventListener(
"load",
()=>{

  updateMusicButton()
  playMusic()

})

document.addEventListener(
"pointerdown",
playMusic,
{ once:true })

document.addEventListener(
"keydown",
playMusic,
{ once:true })

// TYPING EFFECT

const text =
"Every photo with you feels like a beautiful dream ✨"

let i = 0

function typing(){

  if(i < text.length){

    document.getElementById("typing")
    .innerHTML += text.charAt(i)

    i++

    setTimeout(typing,70)

  }

}

typing()

// COUNTDOWN

const target =
new Date("October 5, 2026 00:00:00")
.getTime()

setInterval(()=>{

  const now =
  new Date().getTime()

  const diff = target - now

  const days =
  Math.floor(diff /
  (1000*60*60*24))

  document.getElementById("countdown")
  .innerHTML =
  `${days} days after we will celebrate and create best memories ❤️`

},1000)

// PETALS

const petals =
document.querySelector(".petals")

for(let i=0;i<50;i++){

  let flower =
  document.createElement("span")

  const icons =
  ["🌸","✨","💖","🌷"]

  flower.innerHTML =
  icons[Math.floor(Math.random()*icons.length)]

  flower.style.left =
  Math.random()*100 + "vw"

  flower.style.fontSize =
  15 + Math.random()*25 + "px"

  flower.style.animationDuration =
  5 + Math.random()*10 + "s"

  flower.style.opacity =
  Math.random()

  petals.appendChild(flower)

}

// CURSOR TRAIL

const glow =
document.querySelector(".cursor-glow")

document.addEventListener(
"mousemove",
(e)=>{

  glow.style.left =
  e.clientX + "px"

  glow.style.top =
  e.clientY + "px"

})

// LOVE POPUP

const popup =
document.getElementById("popup")

document.getElementById("loveBtn")
.onclick = ()=>{

  popup.style.display = "flex"

}

function closePopup(){

  popup.style.display = "none"

}

// GSAP ANIMATION

gsap.from(".title",{
  y:-100,
  opacity:0,
  duration:1.5
})

gsap.from("#typing",{
  opacity:0,
  delay:1
})

gsap.from(".memory",{
  opacity:0,
  y:100,
  stagger:0.2,
  duration:1.2
})

gsap.from("video",{
  scale:0.7,
  opacity:0,
  duration:1.5
})

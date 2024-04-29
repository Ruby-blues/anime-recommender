const container = document.querySelector(".video-container");
let video = document.querySelector('video');
let progress_bar = document.querySelector('.progress-bar');
let time_line = document.querySelector('.video-timeline');
let toggle_play = document.querySelector('.toggle-play');
let volume = document.querySelector('.volume');
let volume_slider = document.querySelector('.volume-bar');
const current_video_time = document.querySelector(".current-time")
const duration = document.querySelector(".video-duration")
const fast_forward = document.querySelector('.fast-forward');
const rewind = document.querySelector('.rewind');
const speed_button = document.querySelector('.playback-speed');
const speed_options = document.querySelector('.speed-option-container');
const loop = document.querySelector(".loop");
const pic_in_pic_btn = document.querySelector('.pic-in-pic');
const full_screen = document.querySelector('.fullscreen');
let timer;

progress_bar.defaultValue = 0;
video.preload = "none";

function hideControls() {
    if (video.paused) return;
    timer = setTimeout(() => {
        container.classList.remove("show-controls");
    }, 2000);
}
hideControls();
container.addEventListener("mousemove", () => {
    container.classList.add("show-controls");
    clearTimeout(timer);
    hideControls();
});

function formateTime(time) {
    let seconds = Math.floor(time % 60);
    let minutes = Math.floor(time / 60) % 60;
    let hours = Math.floor(time / 3600);

    seconds = seconds < 10 ? `0${seconds}`: seconds;
    minutes = minutes < 10 ? `0${minutes}`: minutes;
    hours = hours < 10 ? `0${hours}`: hours;

    if (hours == 0) {
        return `${minutes}:${seconds}`;
    }
    return `${hours}:${minutes}:${seconds}`;
}

volume.addEventListener("click", () => {
    if (volume.classList.contains("volume")) {
        volume.classList.replace("volume", "mute");
        volume.src = '/static/icons/mute.svg';
        video.volume = 0;
    } else {
        volume.src = '/static/icons/volume.svg';
        video.volume = 0.5;
        volume.classList.replace("mute", "volume");
    }
    volume_slider.value = video.volume;
});

volume_slider.addEventListener("input", (e) => {
    video.volume = e.target.value;
    if (e.target.value == 0) {
        volume.classList.replace("volume", "mute");
        volume.src = '/static/icons/mute.svg';
    } else {
        volume.classList.replace("mute", "volume");
        volume.src = '/static/icons/volume.svg';
    }
});

loop.addEventListener("click", () => {
    loop.classList.toggle("on");
    if (loop.classList.contains("on")) {
        loop.src = '/static/icons/loop_off.svg';
        video.loop = false;
    } else {
        loop.src = '/static/icons/loop_on.svg';
        video.loop = true;
    }
})

speed_button.addEventListener("click", () => {
    speed_options.classList.toggle("show");
});

speed_options.querySelectorAll("span").forEach(option => {
    option.addEventListener("click", () => {
        video.playbackRate = option.dataset.speed;
        speed_options.querySelector(".active").classList.remove("active");
        option.classList.add("active");
    });
});

document.addEventListener("click", e => {
    if (e.target.tagName == "SPAN") {
        speed_options.classList.remove("show");
    }
});

pic_in_pic_btn.addEventListener("click", () => {
    video.requestPictureInPicture();
});

full_screen.addEventListener("click", () => {
    container.classList.toggle("fullscreen");
    if (document.fullscreenElement) {
        full_screen.src = '/static/icons/fullscreen.svg';
        return document.exitFullscreen();
    }
    full_screen.src = '/static/icons/fullscreen_exit.svg';
    container.requestFullscreen();
});

video.addEventListener("loadeddata", () => {
    duration.innerText = formateTime(video.duration);
});

video.addEventListener('timeupdate', e => {
    let {currentTime, duration} = e.target;
    let percent = (currentTime / duration) * 100;
    progress_bar.value = percent;
    current_video_time.innerText = formateTime(currentTime);
    if (video.ended) {
        toggle_play.src = '/static/icons/play.svg';
    }
});
video.addEventListener("click", play);

function play() {
    if (video.paused) {
        toggle_play.src = "/static/icons/pause.svg";
        console.log(toggle_play.src)
        video.play();
    } else {
        toggle_play.src = "/static/icons/play.svg";
        console.log(toggle_play.src)
        video.pause();
    }

}
progress_bar.addEventListener("input", e => {
    let seconds = video.duration * (e.target.value / 100);
    video.currentTime = seconds;
    current_video_time.innerText = formateTime(video.currentTime);
});

time_line.addEventListener("mousemove", e => {
    const progress_time = time_line.querySelector("span");
    let offset_x = e.offsetX;
    progress_time.style.left = `${offset_x}px`;
    progress_time.innerText = formateTime((offset_x / progress_bar.clientWidth) * video.duration);
});

rewind.addEventListener("click", () => {
    video.currentTime -= 10;
});
fast_forward.addEventListener("click", () => {
    video.currentTime += 10;
});

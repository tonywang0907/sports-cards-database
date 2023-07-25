const progressBar = document.getElementById('progress');
const progressPercentage = progressBar.dataset.progress;
progressBar.style.width = `${progressPercentage}%`;

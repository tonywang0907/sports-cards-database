// JavaScript
  // JavaScript
function toggleIcons(iconType) {
    var starIcon = document.getElementById('star-icon');
    var solidStarIcon = document.getElementById('solid-star-icon');
    var eyeIcon = document.getElementById('eye-icon');
    var eyeSlashIcon = document.getElementById('eye-slash-icon');
    
    if (iconType === 'star') {
        starIcon.classList.toggle('hidden-icon');
        solidStarIcon.classList.toggle('hidden-icon');
        solidStarIcon.classList.toggle('yellow-color');
    } else if (iconType === 'eye') {
        eyeIcon.classList.toggle('hidden-icon');
        eyeSlashIcon.classList.toggle('hidden-icon');
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var fileInput = document.getElementById('import-pic');
    var picContainer = document.getElementById('card-pic-container');
  
    fileInput.addEventListener('change', function() {
        var file = fileInput.files[0];
        var reader = new FileReader();
    
        reader.addEventListener('load', function() {
            var imgElement = document.createElement('img');
            imgElement.src = reader.result;
            imgElement.classList.add('uploaded-image');
            picContainer.innerHTML = '';
            picContainer.appendChild(imgElement);
        });
    
        if (file) {
            reader.readAsDataURL(file);
        }
    });
});
  
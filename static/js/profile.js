document.addEventListener('DOMContentLoaded', () => {
    const imageInput = document.getElementById('id_imagen');
    const preview = document.getElementById('profileDisplay');

    if (imageInput && preview) {
        imageInput.onchange = () => {
            const [file] = imageInput.files;
            if (file) {
                preview.src = URL.createObjectURL(file);
            }
        };
    }
});
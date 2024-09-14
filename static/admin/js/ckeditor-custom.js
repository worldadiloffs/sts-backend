ClassicEditor
    .create(document.querySelector('#editor'), {
        licenseKey: 'RVRWTnkwcDdPTkVUVWtacER1dkxpUXYxa3dGOE9TeEF2VGVzczVJMG9BQWIzWkpCSnJYY1JJV2oxcWd6UVE9PS1NakF5TkRFd01UUT0=',
        toolbar: [ 'heading', '|', 'bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote' ],
        // Boshqa kerakli sozlamalar
    })
    .catch(error => {
        console.error('CKEditor ishlashida xatolik yuz berdi:', error);
    });
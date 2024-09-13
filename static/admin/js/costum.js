document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM fully loaded and parsed');
    var superCategoryField = document.getElementById('id_super_category');
    var mainCategoryField = document.getElementById('id_main_category');
    var subCategoryField = document.getElementById('id_sub_category');
    console.log(mainCategoryField)

    superCategoryField.addEventListener('change', function () {
        var superCategoryId = this.value;

        if (superCategoryId) {
            fetch(`/get_main_categories/?super_category=${superCategoryId}`)
            .then(response => response.json())
            .then(data => {
                var options = '<option value="" selected="selected">---------</option>';
                data.forEach(function (item) {
                    options += `<option value="${item.id}">${item.name}</option>`;
                });
                mainCategoryField.innerHTML = options;
            })
            .catch(error => {
                console.error('Error fetching main categories:', error);
            });
               
                
        
        } else {
            mainCategoryField.innerHTML = '<option value="" selected="selected">---------</option>';
            subCategoryField.innerHTML = '<option value="" selected="selected">---------</option>';
        }
    });
    

    mainCategoryField.addEventListener('change', function () {
        var mainCategoryId = this.value;

        if (mainCategoryId) {
            fetch(`/get_sub_categories/?main_category=${mainCategoryId}`)
                .then(response => response.json())
                .then(data => {
                    var options = '<option value="" selected="selected">---------</option>';
                    data.forEach(function (item) {
                        options += `<option value="${item.id}">${item.name}</option>`;
                    });
                    subCategoryField.innerHTML = options;
                });
        } else {
            subCategoryField.innerHTML = '<option value="" selected="selected">---------</option>';
        }
    });
});

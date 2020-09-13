/* vl Scripts */

$(function () {

    /*
        Our anonymous functions
    *   We create it to reuse it pretty simple
        The way is that we want to respect DRY philosophy
    * */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                 $("#windows-modal").modal("show");
            },
            success: function (data) {
                $("#windows-modal").find(".modal-content").html(data.html_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        // Here we use formdata object because we manipulate file.
        // If not we can use something like this
        /*
        * var saveForm = function () {
        *   var form = $(this);
            $.ajax({
                url: form.attr("action"),
                data: form.serialize(),
                type: form.attr("method"),
                dataType: 'json',
                success: function (data) {
                    if (data.form_is_valid) {
                        $("#project-table tbody").html(data.----);
                        $("#modal-project").modal("hide");
                } else {
                    $("#modal-project .modal-content").html(data.----);
                }
            }
        });
        return false;
        };
        * */
        var formData = new FormData(form[0]);
        $.ajax({
            url: form.attr("action"),
            data: formData,
            type: form.attr("method"),
            dataType: 'json',
            async: true,
            cache: false,
            contentType: false,
            enctype: form.attr("enctype"),
            processData: false,

            success: function (data) {
                if (data.form_is_valid) {
                    $("#vl-table tbody").html(data.html_list);
                    $("#windows-modal").modal("hide");
                    swal({
                        title: data.messages.title,
                        text: data.messages.text,
                        type: data.messages.icon
                    },
                        function (isConfirm) {
                            if (isConfirm) {
                                location.reload(true);
                            }
                        }
                        );
                }
                else {
                    $("#windows-modal").find(".modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Littles bindings
    *  ==== Note ====
    * We are aware that the exercise was only to add functionality
    * for project creation but we take the risk of adding more choices
    * to allow the end user to have a more complete set of features
    * allowing him to better manipulate his files.
    */
    // Add Project
    $(".add-vl").click(loadForm);
    $("#windows-modal").on("submit", ".add-vl-form", saveForm);

    // Update vl
    $("#vl-table").on("click", ".edit-vl-btn", loadForm);
    $("#windows-modal").on("submit", ".js-vl-update-form", saveForm);

    // Delete vl
    $("#vl-table").on("click", ".delete-vl-btn", loadForm);
    $("#windows-modal").on("submit", ".js-vl-delete-form", saveForm);
});
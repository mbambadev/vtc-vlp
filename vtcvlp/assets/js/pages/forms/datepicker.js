'use strict';
$(function () {

    //Datetimepicker plugin
    $('.datepicker').bootstrapMaterialDatePicker({
        lang: 'fr',
        cancelText: 'ANNULER',
        year: true,
        minDate: moment("1939-12-31"),
        maxDate: moment("2003-12-31"),
        monthPicker: true,
        time: false
    });
});
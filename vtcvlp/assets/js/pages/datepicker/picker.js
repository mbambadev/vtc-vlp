/* Promise datetime picker scripts js */

/*Domain Init*/
"use strict";
$(function () {
     $("#date-dropper-picker").datetimepicker(
         {

             minDate: moment(),
             format: 'd/m/Y H:i',
             locale: 'fr',
             i18n: {
                 fr: {
                     months: [
                         'Janvier', 'Fevrier', 'Mars', 'Avril',
                         'Mai', 'Juin', 'Juillet', 'Août',
                         'Septembre', 'Octobre', 'Novembre', 'Decembre',
                     ],
                     dayOfWeek: [
                         "Lundi.", "Mardi", "Mercredi", "Jeudi",
                         "Vendredi", "Samedi", "Dimanche",
                     ]
                 }
             },
             startDate: moment(),
             mask: true,
         }
     );
});

/*
Due to limitations in materialize i am unable to change the code below to prevent any errors
when passed through jslint without hindering my application. I managed to remove these errors
however the javascript elements in my application stopped working as a result. This code below
is structured as instructed by materialize.css in order for all elements below to work correctly.
*/

document.addEventListener('DOMContentLoaded', function() {
    //sidenav initialisation
    let sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav);

    //delete modal inititalisation
    let modal = document.querySelectorAll('.modal');
    M.Modal.init(modal);

    // select dropdown menu initialisation
    let select = document.querySelectorAll('select');
    M.FormSelect.init(select);

    // collapsible accordian initialisation
    collapsible = document.querySelectorAll('.collapsible');
    M.Collapsible.init(collapsible);

  });
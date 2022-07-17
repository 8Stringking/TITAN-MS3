let M;

let Collapsible;

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
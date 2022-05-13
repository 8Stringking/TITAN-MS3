document.addEventListener('DOMContentLoaded', function() {
    //sidenav initialisation
    let sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav);
    //delete modal inititalisation
    let modal = document.querySelectorAll('.modal');
    M.Modal.init(modal);
  });
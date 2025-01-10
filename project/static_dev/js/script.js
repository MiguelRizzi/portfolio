//_____________________ NAVBAR____________________
// Bootstrap ScrollSpy
window.addEventListener('scroll', function() {
    var navbar = document.querySelector('.navbar');
    var aNavbarBrand = document.querySelector('.a-navbar-brand');
    var scrolled = window.scrollY || document.documentElement.scrollTop;
    const currentPath = window.location.pathname;

    if (scrolled > 0) {
        navbar.classList.add('navbar-scroll');
        aNavbarBrand.classList.remove('d-none');

        
    } else {
        navbar.classList.remove('navbar-scroll');
        aNavbarBrand.classList.add('d-none');
        if (currentPath !== '/' && currentPath !== '/blog/' && currentPath !== '/portfolio/') {
            aNavbarBrand.classList.remove('d-none');
        }
             
    }
});


//____________________ ANIMACIONES GSAP SCROLLTRIGGER____________________

// funcion para animar teniendo segun la direccion
function direccionAnimacion(elem, direction) {
    direction = direction || 1;
    var x = 0,
        y = direction * 100;

    // Determina las coordenadas de traducción según la dirección
    if (elem.classList.contains("izquierda")) {
        x = -100;
        y = 0;
    } else if (elem.classList.contains("derecha")) {
        x = 100;
        y = 0;
    }

    elem.style.transform = "translate(" + x + "px, " + y + "px)";
    elem.style.opacity = "0";

    // animacion
    gsap.fromTo(elem, { x: x, y: y, autoAlpha: 0 }, {
        duration: 2.5,
        x: 0,
        y: 0,
        autoAlpha: 1,
        ease: "expo",
        overwrite: "auto"
    });
}

// funcion para ocultar el elemento
function ocultar(elem) {
    gsap.set(elem, { autoAlpha: 0 });
}

document.addEventListener("DOMContentLoaded", function () {
    if (window.matchMedia("(min-width: 1200px)").matches) {
        gsap.registerPlugin(ScrollTrigger);

        // ScrollTriger para cada elemento con la clase .revelar     
        gsap.utils.toArray(".revelar").forEach(function (elem) {
            ScrollTrigger.create({
                trigger: elem,
                markers: false,
                onEnter: function () { direccionAnimacion(elem) }, // anima el elemento al entrar en la vista
                onEnterBack: function () { direccionAnimacion(elem, -1) }, // anima el elemento al retroceder a la vista
                onLeave: function () { ocultar(elem) } // oculta el elemento al salir de la vista
            });
        });
    }
});

//____________________ MODAL CON HTMX ______________________
(function () {
    const modal = new bootstrap.Modal(document.getElementById("modal"))
    
    htmx.on("htmx:afterSwap", (e) => {
      // Response targeting #dialog => show the modal
      if (e.detail.target.id == "dialog") {
        modal.show()
      }
    })
    
    htmx.on("htmx:beforeSwap", (e) => {
      // Empty response targeting #dialog => hide the modal
      if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
        modal.hide()
        e.detail.shouldSwap = false
      }
    })
    
    // Remove dialog content after hiding
    htmx.on("hidden.bs.modal", () => {
      document.getElementById("dialog").innerHTML = ""
    })
  
    
})();

//____________________ TOAST CON HTMX ______________________

(function () {
    const toastElement = document.getElementById("toast")
    const toastBody = document.getElementById("toast-body")
    const toast = new bootstrap.Toast(toastElement, { delay: 5000 })
  
    htmx.on("showMessage", (e) => {
      toastBody.innerText = e.detail.value
      toast.show()
    })
})();


//____________________ FOOTER YEAR ______________________
  const yearElement = document.getElementById("year");
  const currentYear = new Date().getFullYear();
  yearElement.textContent = currentYear;

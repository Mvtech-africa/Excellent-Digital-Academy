
//-----------------------Show / Hide menu bar-----------------

document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.getElementById("menu-toggle");
  const closeMenu = document.getElementById("close-menu");
  const openIcon = document.getElementById("open-icon");
  const closeIcon = document.getElementById("close-icon");
  const popupMenu = document.getElementById("popup-menu");
  

  // Toggle menu with main button
  menuToggle.addEventListener("click", () => {
    toggleMenu();
  });

  // Close menu with close button inside menu
  closeMenu.addEventListener("click", () => {
    toggleMenu(true);
  });


  

  // Function to toggle menu visibility
  function toggleMenu(forceClose = false) {
    const isOpen = popupMenu.classList.contains("open");

    if (isOpen || forceClose) {
      popupMenu.classList.remove("open");
      openIcon.classList.add("visible");
      closeIcon.classList.remove("visible");
    } else {
      popupMenu.classList.add("open");
      openIcon.classList.remove("visible");
      closeIcon.classList.add("visible");
    }
  }
});







const dropdownBtns = document.querySelectorAll(".dropdown-btn");  


 // to show dropdown list

        dropdownBtns.forEach(btn => {  
        btn.addEventListener("click", function() {  
                this.classList.toggle("active");  
                const dropdownContent = this.nextElementSibling;  

                if (dropdownContent.style.display === "block") {  
                    dropdownContent.style.display = "none";  
                    this.querySelector('.drop-icon').classList.remove('rotate2');  
                } else {  
                    dropdownContent.style.display = "block";  
                    this.querySelector('.drop-icon').classList.add('rotate2');  
                }  

            });  
        });  









        window.addEventListener('scroll', function() {  
            const header = document.querySelector('.header-bg');  
                if (window.scrollY > 50) { // Adjust the scroll threshold as needed  
                    header.classList.add('scrolled');  
                } else {  
                    header.classList.remove('scrolled');  
                }  
            });  

































// ----------------------- Hero Section Slider -----------------


    const slidesTrack = document.getElementById('slides');
    const slideEls = document.querySelectorAll('.slide');
    const prevBtn = document.getElementById('prev');
    const nextBtn = document.getElementById('next');
    const dotsWrap = document.getElementById('dots');

    let index = 0;
    const count = slideEls.length;
    const intervalMs = 4000;
    let timer = null;

    // Build dots dynamically
    const dots = Array.from({ length: count }, (_, i) => {
        const dot = document.createElement('button');
        dot.className = 'dot' + (i === 0 ? ' active' : '');
        dot.addEventListener('click', () => { goTo(i); restart(); });
        dotsWrap.appendChild(dot);
        return dot;
    });

    function goTo(i) {
        index = (i + count) % count;
        slidesTrack.style.transform = `translateX(-${index * 100}%)`;
        dots.forEach((d, j) => d.classList.toggle('active', j === index));
    }

    function nextSlide() { goTo(index + 1); }
    function prevSlide() { goTo(index - 1); }

    function start() { timer = setInterval(nextSlide, intervalMs); }
    function stop() { clearInterval(timer); }
    function restart(){ stop(); start(); }

    nextBtn.addEventListener('click', () => { nextSlide(); restart(); });
    prevBtn.addEventListener('click', () => { prevSlide(); restart(); });

    // Init
    goTo(0);
    start();














































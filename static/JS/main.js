
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




































    
















    

/*----------------------form reveal password toggle icon code------------------------------------*/

function togglePassword() {
  var passwordField = document.getElementById("password");
  var toggleIcon = document.getElementById("toggle-icon");

  if (passwordField.type === "password") {

      passwordField.type = "text";
      toggleIcon.classList.remove("fa-eye");
      toggleIcon.classList.add("fa-eye-slash");
  } 
  
  else {
      passwordField.type = "password";
      toggleIcon.classList.remove("fa-eye-slash");
      toggleIcon.classList.add("fa-eye");
  }
}
















// --------------------- courses carousel code ----------------------------------


 const carousel = document.getElementById("carousel");
  const items = document.querySelectorAll(".carousel-item");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");

  let index = 0;
  let interval;

  function getItemWidth() {
    return items[0].offsetWidth + 20; // width + gap
  }

  function goToSlide(i) {
    index = Math.max(0, Math.min(i, items.length - 1));
    carousel.style.transform = `translateX(${-index * getItemWidth()}px)`;
  }

  function nextSlide() {
    if (index < items.length - 1) {
      index++;
      goToSlide(index);
    } else {
      index = 0; // loop back
      goToSlide(index);
    }
  }

  function prevSlide() {
    if (index > 0) {
      index--;
      goToSlide(index);
    } else {
      index = items.length - 1; // loop back
      goToSlide(index);
    }
  }

  function autoSlide() {
    interval = setInterval(nextSlide, 5000);
  }

  function resetAutoSlide() {
    clearInterval(interval);
    autoSlide();
  }

  nextBtn.addEventListener("click", () => { nextSlide(); resetAutoSlide(); });
  prevBtn.addEventListener("click", () => { prevSlide(); resetAutoSlide(); });

  autoSlide();

  // Recalculate slide width on resize
  window.addEventListener("resize", () => goToSlide(index));




























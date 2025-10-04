
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

dropdownBtns.forEach(btn => {
  btn.addEventListener("click", function () {
    const dropdownContent = this.nextElementSibling;
    const icon = this.querySelector('.drop-icon');

    // Close all other dropdowns
    dropdownBtns.forEach(otherBtn => {
      if (otherBtn !== this) {
        otherBtn.classList.remove("active");
        const otherContent = otherBtn.nextElementSibling;
        const otherIcon = otherBtn.querySelector('.drop-icon');

        if (otherContent) otherContent.style.display = "none";
        if (otherIcon) otherIcon.classList.remove('rotate2');
      }
    });

    // Toggle the clicked one
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
      icon.classList.remove('rotate2');
    } else {
      dropdownContent.style.display = "block";
      icon.classList.add('rotate2');
    }

    this.classList.toggle("active");
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

















  //  partner section Drag-to-scroll
const slider = document.querySelector('.partner-main-con');
let isDown = false;
let startX;
let scrollLeft;

slider.addEventListener('mousedown', (e) => {
  isDown = true;
  slider.classList.add('active');
  startX = e.pageX - slider.offsetLeft;
  scrollLeft = slider.scrollLeft;
});
slider.addEventListener('mouseleave', () => { isDown = false; });
slider.addEventListener('mouseup', () => { isDown = false; });
slider.addEventListener('mousemove', (e) => {
  if(!isDown) return;
  e.preventDefault();
  const x = e.pageX - slider.offsetLeft;
  const walk = (x - startX) * 2; // scroll-fast
  slider.scrollLeft = scrollLeft - walk;
});

// Auto scroll
function autoScroll() {
  if (slider.scrollLeft + slider.clientWidth >= slider.scrollWidth) {
    slider.scrollLeft = 0;
  } else {
    slider.scrollLeft += 1; // speed
  }
}
let scrollInterval = setInterval(autoScroll, 20);

// Pause auto-scroll on hover
slider.addEventListener('mouseenter', () => clearInterval(scrollInterval));
slider.addEventListener('mouseleave', () => scrollInterval = setInterval(autoScroll, 20));


























// -------------------- scroll counter -------------------------------------


(function() {
  // If IntersectionObserver isn't supported, fallback to immediate count
  const supportsObserver = 'IntersectionObserver' in window;

  const easeFunctions = {
    // Simple easing options
    linear: t => t,
    // easeOutQuad: decelerating to 1
    easeOutQuad: t => 1 - (1 - t) * (1 - t),
    // you can add more if you want
  };

  function animateCount(el, target, duration, easeName) {
    const start = 0;
    const startTime = performance.now();
    const ease = (easeFunctions[easeName] || easeFunctions.linear);

    function tick(now) {
      const elapsed = now - startTime;
      const t = Math.min(elapsed / duration, 1);
      const value = Math.floor(start + (target - start) * ease(t));
      el.textContent = value.toLocaleString();
      if (t < 1) {
        requestAnimationFrame(tick);
      } else {
        el.textContent = target.toLocaleString();
        el.dataset.ended = 'true';
      }
    }

    requestAnimationFrame(tick);
  }

  function initCounter(el) {
    // If already ended, skip
    if (el.dataset.ended === 'true') return;
    const target = parseInt(el.getAttribute('data-count') || '0', 10);
    const duration = parseInt(el.getAttribute('data-duration') || '2000', 10);
    const easeName = el.getAttribute('data-easing') || 'linear';
    // Start from 0 (or keep current value if you want)
    el.textContent = '0';
    animateCount(el, target, duration, easeName);
  }

  const elements = Array.from(document.querySelectorAll('.js-scroll-counter'));

  if (supportsObserver) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          initCounter(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, {
      root: null,
      rootMargin: '0px',
      threshold: 0.25 // start when ~25% visible
    });

    elements.forEach(el => observer.observe(el));
  } else {
    // Fallback: count immediately for browsers without IntersectionObserver
    elements.forEach(el => initCounter(el));
  }
})();

































































  // --------------------- testimonials ----------------------

 
    (function(){
      const track = document.getElementById('testimonials');
      let isDown = false;
      let startX;
      let scrollLeft;
      let velocity = 0;
      let rafId = null;

      track.addEventListener('pointerdown', (e) => {
        isDown = true;
        track.setPointerCapture(e.pointerId);
        startX = e.clientX;
        scrollLeft = track.scrollLeft;
        velocity = 0;
        track.classList.add('dragging');
        e.preventDefault();
      });

      track.addEventListener('pointermove', (e) => {
        if(!isDown) return;
        const x = e.clientX;
        const walk = (startX - x);
        const prev = track.scrollLeft;
        track.scrollLeft = scrollLeft + walk;
        velocity = track.scrollLeft - prev;
      });

      function stopDrag(e){
        if(!isDown) return;
        isDown = false;
        try{ if(e && e.pointerId) track.releasePointerCapture(e.pointerId); }catch(_){}
        track.classList.remove('dragging');
        cancelAnimationFrame(rafId);
        const step = () => {
          if(Math.abs(velocity) < 0.3) return;
          track.scrollLeft += velocity;
          velocity *= 0.93;
          rafId = requestAnimationFrame(step);
        };
        rafId = requestAnimationFrame(step);
      }
      track.addEventListener('pointerup', stopDrag);
      track.addEventListener('pointercancel', stopDrag);
      track.addEventListener('pointerleave', stopDrag);

      const btnLeft = document.querySelector('.arrow.left');
      const btnRight = document.querySelector('.arrow.right');
      const cardWidth = 320;
      btnLeft.addEventListener('click', ()=>{
        track.scrollBy({left: -cardWidth, behavior:'smooth'});
      });
      btnRight.addEventListener('click', ()=>{
        track.scrollBy({left: cardWidth, behavior:'smooth'});
      });

      window.addEventListener('keydown',(e)=>{
        if(e.key === 'ArrowLeft') track.scrollBy({left:-cardWidth,behavior:'smooth'});
        if(e.key === 'ArrowRight') track.scrollBy({left:cardWidth,behavior:'smooth'});
      });

      const fadeLeft = document.querySelector('.fade.left');
      const fadeRight = document.querySelector('.fade.right');
      function updateFades(){
        const maxScroll = track.scrollWidth - track.clientWidth;
        fadeLeft.style.display = track.scrollLeft > 8 ? 'block' : 'none';
        fadeRight.style.display = track.scrollLeft < maxScroll - 8 ? 'block' : 'none';
      }
      track.addEventListener('scroll', updateFades);
      window.addEventListener('resize', updateFades);
      updateFades();

      track.querySelectorAll('img').forEach(img=>{ img.draggable = false });
      document.querySelectorAll('.card').forEach(card=> card.setAttribute('tabindex','0'));
    })();









    // footer current year for copy right


    document.getElementById("year").textContent = new Date().getFullYear();







    // -------------------multi tab -----------------------

    const tabs = document.querySelectorAll(".tab");
    const contents = document.querySelectorAll(".tab-content");

    tabs.forEach(tab => {
      tab.addEventListener("click", () => {
        // Remove active class from all
        tabs.forEach(t => t.classList.remove("active"));
        contents.forEach(c => c.classList.remove("active"));

        // Add active class to clicked tab and related content
        tab.classList.add("active");
        document.getElementById(tab.dataset.tab).classList.add("active");
      });
    });


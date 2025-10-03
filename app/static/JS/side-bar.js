// // -------------------------------  Side bar --------------------------------------


const dropdownBtns = document.querySelectorAll(".dropdown-btn");  
const sidebar = document.getElementById("mySidebar");  
const content = document.getElementById("myContent");  
const toggleBtn = document.getElementById("toggleBtn");  
const openIcon = toggleBtn.querySelector('.open');  
const closeIcon = toggleBtn.querySelector('.close');  




        // to show dropdown list

        dropdownBtns.forEach(btn => {  
        btn.addEventListener("click", function() {  
                this.classList.toggle("active");  
                const dropdownContent = this.nextElementSibling;  

                if (dropdownContent.style.display === "block") {  
                    dropdownContent.style.display = "none";  
                    this.querySelector('i.uis-down').classList.remove('rotate2');  
                } else {  
                    dropdownContent.style.display = "block";  
                    this.querySelector('i.uis-down').classList.add('rotate2');  
                }  

            });  
        });  




    // To hide and show side bar

        toggleBtn.addEventListener("click", function() {  
        sidebar.classList.toggle("hidden");  
        content.classList.toggle("collapsed");  
        this.classList.toggle("collapsed");  

        if (sidebar.classList.contains("hidden")) {  
            openIcon.style.display = 'none';  
            closeIcon.style.display = 'inline-block';  
                //toggleBtn.style.left = '10px'; // Move toggle button to the left 
            } else {  
                openIcon.style.display = 'inline-block';  
                closeIcon.style.display = 'none'; 
                //toggleBtn.style.left = '10px'; // Reset toggle button position   
            }  
        });  


    


            // Initialize the icons' visibility and toggle button position
            
            
            if (sidebar.classList.contains("hidden")) {  
                openIcon.style.display = 'none';  
                closeIcon.style.display = 'inline-block';  
            } else {  
                openIcon.style.display = 'inline-block';  
                closeIcon.style.display = 'none';   
            }  
























 // --------------------------------copy right code--------------------------

document.getElementById("year").textContent = new Date().getFullYear();
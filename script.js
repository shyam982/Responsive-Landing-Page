// Navbar color change on scroll

window.addEventListener("scroll",function(){


    let navbar=document.getElementById("navbar");


    if(window.scrollY > 50)

    {

        navbar.classList.add("scrolled");

    }


    else

    {

        navbar.classList.remove("scrolled");

    }


});





// Explore More button

function exploreMore(){


    document.getElementById("services").scrollIntoView({

        behavior:"smooth"

    });


}
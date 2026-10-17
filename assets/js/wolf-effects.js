/**
 * WOLF-EFFECTS.JS
 * Master logic for all Wolvatarr pages
 */

// --- 1. THE WOLF HOWL (Wild Animation Version) ---
function playWolfHowl() {
    const howl = document.getElementById('wolfHowlAudio');
    if (howl) {
        howl.currentTime = 0;
        howl.play().catch(e => console.log("Audio play blocked until user interaction."));
        
        // High-energy surge feedback
        const trigger = document.querySelector('.howl-trigger');
        if (trigger) {
            trigger.classList.add('electric-surge');
            setTimeout(() => trigger.classList.remove('electric-surge'), 500);
        }
    }
}

// --- 2. GLOBAL UI EFFECTS (Loader & Mouse) ---
window.addEventListener('load', () => {
    const loader = document.getElementById('loader');
    if (loader) {
        setTimeout(() => {
            loader.style.opacity = '0';
            setTimeout(() => { loader.style.visibility = 'hidden'; }, 800);
        }, 3000);
    }
});

document.addEventListener('mousemove', (e) => {
    const x = (e.clientX / window.innerWidth) * 100;
    const y = (e.clientY / window.innerHeight) * 100;
    document.documentElement.style.setProperty('--mouse-x', x + '%');
    document.documentElement.style.setProperty('--mouse-y', y + '%');
});

// --- 3. SCROLL & BACK TO TOP ---
const backToTop = document.getElementById("backToTop");
window.onscroll = function() {
    if (backToTop) {
        if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
            backToTop.classList.add("show");
        } else {
            backToTop.classList.remove("show");
        }
    }
};

function initiateBeam(e) {
    if (e) e.preventDefault();
    if (backToTop) {
        backToTop.classList.add('electric-surge');
        window.scrollTo({ top: 0, behavior: 'smooth' });
        setTimeout(() => {
            backToTop.classList.remove('electric-surge');
        }, 600);
    }
}

// --- 4. CONTACT FORM HANDLER ---
// Only runs if the form exists on the page
const contactForm = document.getElementById('wolfContactForm');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const btn = this.querySelector('.btn-submit');
        btn.innerHTML = "TRANSMITTING...";
        btn.style.opacity = "0.7";
        setTimeout(() => {
            alert("Transmission Received. The Wolf will be in touch shortly.");
            btn.innerHTML = "SEND TRANSMISSION";
            btn.style.opacity = "1";
            this.reset();
        }, 2000);
    });
}